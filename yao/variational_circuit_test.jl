using JSON,Base.Threads
using BenchmarkTools
using Yao,YaoBlocks, Yao.EasyBuild
using Yao, Yao.AD
using DataFrames
using CSV
using KrylovKit: eigsolve
mark = "Yao"
const nqubit_list = 12:26
const benchmarks = Dict()


function build_circuit(L::Int)
	depth = 10
	circuit = chain(L)
	for i in 1:L
        push!(circuit, chain(L, put(i=>Rz(randn()))))
		push!(circuit, chain(L, put(i=>Ry(randn()))))
        push!(circuit, chain(L, put(i=>Rz(randn()))))
    end
	for i in 1:depth
		if isodd(i)
			for j in 1:(L-1)
		    	push!(circuit, control(j, (j+1)=>X))
            end
		else
			for j in (L-1):-1:1
		    	push!(circuit, control(j, (j+1)=>X))
			end			
		end
		for j in 1:L
			push!(circuit, chain(L, put(j=>Rz(randn()))))
			push!(circuit, chain(L, put(j=>Ry(randn()))))
            push!(circuit, chain(L, put(j=>Rz(randn()))))
		end
	end
	return circuit	
end

# function heisenberg(n)
# 	bond(n, i) = sum([put(n, i=>σ) * put(n, i+1=>σ) for σ in (X, Y, Z)])
# 	return sum([bond(n, i) for i in 1:n-1]);
# end


function ad_excute(circuit, state, ham)
	grads = expect'(ham, state=>circuit)
end


# function noiseless_derivation_performance(n::Int)
# 	#n_params_count = (depth+1)*n*3
# 	state = zero_state(n)
#     ham = heisenberg(n)
# 	circuit = dispatch!(build_circuit(n),:random)

# 	t = @elapsed expect'(ham, state=>circuit)
# 	return t 
# end


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
		t = @benchmark $(zero_state(k)) |> $(build_circuit(k))
        data = (mean(t).time/1e9, std(t).time/1e9, minimum(t).time/1e9, maximum(t).time/1e9)
    end
end


@task "ad" nqubits=nqubit_list begin
    map(nqubit_list) do k
        t = @benchmark ad_excute($(dispatch!(build_circuit(k),:random)), $(zero_state(k)), $(heisenberg(k)))
        data = (mean(t).time/1e9, std(t).time/1e9, minimum(t).time/1e9, maximum(t).time/1e9)
    end
end

if !ispath("./.benchmarks/Linux-CPython-3.9-64bit")
    mkpath("./.benchmarks/Linux-CPython-3.9-64bit")
end

write("./.benchmarks/Linux-CPython-3.9-64bit/variational_circuit_test.json", JSON.json(benchmarks,4))