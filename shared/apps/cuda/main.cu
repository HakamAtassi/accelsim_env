#include <iostream>

// CUDA kernel function
__global__ void helloFromGPU() {
    printf("Hello World from GPU thread %d!\n", threadIdx.x);
}

int main() {
    std::cout << "Hello World from CPU!" << std::endl;

    // Launch kernel with 1 block of 5 threads
    helloFromGPU<<<1, 5>>>();

    // Wait for GPU to finish before accessing results
    cudaDeviceSynchronize();

    return 0;
}
