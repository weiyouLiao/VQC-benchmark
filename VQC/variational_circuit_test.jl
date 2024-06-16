using JSON, Base.Threads
using BenchmarkTools
using VQC, VQC.Utilities, Zygote
using QuantumCircuits 
import MPSSimulator.fuse_gates
using CSV
using Random
mark = "VQC"
const nqubit_list = 12:28
const benchmarks = Dict()

function build_circuit(L::Int)
	depth = 10
	circuit = QCircuit()
	for i in 1:L
		push!(circuit, RzGate(i, randn()*2π, isparas=false))
		push!(circuit, RyGate(i, randn()*2π, isparas=false))
		push!(circuit, RzGate(i, randn()*2π, isparas=false))
	end		
	for i in 1:depth
		if isodd(i)
			for j in 1:(L-1)
		    	push!(circuit, CNOTGate(j, j+1))
			end
		else
			for j in (L-1):-1:1
		    	push!(circuit, CNOTGate(j, j+1))
			end			
		end
		for j in 1:L
			push!(circuit, RzGate(j, randn()*2π, isparas=false))
			push!(circuit, RyGate(j, randn()*2π, isparas=false))
			push!(circuit, RzGate(j, randn()*2π, isparas=false))
		end
	end
	circuit = fuse_gates(circuit)
	return circuit	
end



function ad_excute(circuit, state, ham)
	loss(circ) = real(expectation(ham, circ * state))
	gradient(loss, circuit)
end


# function noiseless_derivation_performance(n::Int, depth::Int)
# 	state = StateVector(ComplexF32, n)
# 	ham = heisenberg_1d(n)
# 	circuit = variational_circuit_1d(n, depth)
# 	circuit = fuse_gates(circuit)
# 	loss(circ) = real(expectation(ham, circ * state))
# 	gradient(loss, circuit)
# 	return t 
# end
# heisenberg_1d(n)

macro task(name::String, nqubits_ex, body)
    nqubits = nqubits_ex.args[2]
	msg = "benchmarking $name"
    quote
        @info $msg
        benchmarks[$(name)] = Dict()
        benchmarks[$(name)]["nqubits"] = $(esc(nqubits))
        benchmarks[$(name)]["meantimes"] = []
        benchmarks[$(name)]["stdtimes"] = []
        benchmarks[$(name)]["minimumtimes"] = []
        benchmarks[$(name)]["maximumtimes"] = []
        for result in $(esc(body))
            push!(benchmarks[$(name)]["meantimes"],  result[1])
            push!(benchmarks[$(name)]["stdtimes"], result[2])
            push!(benchmarks[$(name)]["minimumtimes"], result[3])
            push!(benchmarks[$(name)]["maximumtimes"], result[4])
        end

    end
end


@task "vqc" nqubits=nqubit_list begin
    map(nqubit_list) do k
        t = @benchmark apply!($(build_circuit(k)), $(StateVector(ComplexF32, k)))
        data = (mean(t).time/1e9, std(t).time/1e9, minimum(t).time/1e9, maximum(t).time/1e9)
    end
end

@task "ad" nqubits=nqubit_list begin
    map(nqubit_list) do k

        t = @benchmark ad_excute($(fuse_gates(variational_circuit_1d(k, 10))), $(StateVector(ComplexF32, k)), $(heisenberg_1d(k)))
        data = (mean(t).time/1e9, std(t).time/1e9, minimum(t).time/1e9, maximum(t).time/1e9)
    end
end

if !ispath("./.benchmarks/Linux-CPython-3.9-64bit")
    mkpath("./.benchmarks/Linux-CPython-3.9-64bit")
end

write("./.benchmarks/Linux-CPython-3.9-64bit/variational_circuit_test.json", JSON.json(benchmarks,4))









