using JSON, Base.Threads
using BenchmarkTools
using VQC, VQC.Utilities, Zygote
using QuantumCircuits
import MPSSimulator.fuse_gates
using CSV
using Random
benchmarks = Dict()
BenchmarkTools.DEFAULT_PARAMETERS.seconds = 500
BenchmarkTools.DEFAULT_PARAMETERS.samples = 1
BenchmarkTools.DEFAULT_PARAMETERS.evals = 1

const nqubit_list = [26]


function build_circuit(L::Int)
    depth = 10
    circuit = QCircuit()
    for i in 1:L
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


thread_count = Threads.nthreads()
key = "vqc_thread$(thread_count)"

benchmarks[key] = Dict(
    "thread" => string(thread_count),
    "nqubits" => nqubit_list,
    "meantimes" => Float64[],
    "stdtimes" => Float64[],
    "minimumtimes" => Float64[],
    "maximumtimes" => Float64[]
)

# 为当前线程计数填充基准测试结果
for nqubit in nqubit_list
    result = @benchmark apply!($(build_circuit(nqubit)), $(StateVector(ComplexF32, nqubit)))
    push!(benchmarks[key]["meantimes"], mean(result).time/1e9)
    push!(benchmarks[key]["stdtimes"], std(result).time/1e9)
    push!(benchmarks[key]["minimumtimes"], minimum(result).time/1e9)
    push!(benchmarks[key]["maximumtimes"], maximum(result).time/1e9)
end


function read_and_append_json(filename, new_data)
    # 初始化一个空字典来保存现有数据
    existing_data = Dict()

    # 检查文件是否存在以及是否为空
    if isfile(filename) && filesize(filename) > 0
        try
            # 尝试解析JSON文件
            existing_data = JSON.parsefile(filename)
        catch e
            # 如果解析失败，输出错误信息并从空字典开始
            println("解析JSON文件时出错", e)
        end
    end

    # 将新数据合并到现有数据中
    existing_data = merge(existing_data, new_data)

    # 将更新后的数据转换为JSON格式的字符串
    json_str = JSON.json(existing_data,4)

    # 将JSON字符串写入文件
    open(filename, "w") do io
        write(io, json_str)
    end
end
new_data = Dict(key => benchmarks[key])

filename = "./.benchmarks/Linux-CPython-3.9-64bit/parallelization_performance.json"


read_and_append_json(filename, new_data)
