import ray
import dask.array as da

def test_dask_and_ray_working():
    # Dask test
    arr = da.ones((1000, 1000), chunks=(250, 250))
    total = arr.sum().compute()
    assert total == 1_000_000

    # Ray test
    ray.init(ignore_reinit_error=True)

    @ray.remote
    def square(x):
        return x * x

    result = ray.get(square.remote(4))
    assert result == 16

    ray.shutdown()