# Overwhelming the CPU with Flask and ApacheBench

In this repository, we demonstrate how to push the limits of CPU utilization using a Flask application and the ApacheBench (ab) tool. The primary aim is to observe and understand system behavior under stress.

## 1. Installation Requirements

Before starting with the experiments, ensure you have the necessary tools and libraries installed:

- **Flask**: The micro web framework for Python.
  
  ```bash
  pip3 install Flask
  ```

- **Gunicorn**: The WSGI server to serve the Flask application.
  
  ```bash
  pip3 install gunicorn3
  ```

- **ApacheBench**: Typically comes pre-installed with the Apache HTTP server package. Depending on your system, you might need to install the Apache HTTP server or use a package manager specific command.

- **ApacheBench on WSL**:

  If you're using the Windows Subsystem for Linux, ApacheBench can be easily installed using the package manager of your specific Linux distribution. Here's how to do it for some common distributions:

  - **Ubuntu/Debian**:

    ```bash
    sudo apt update
    sudo apt install apache2-utils
    ```

  - **Fedora**:

    ```bash
    sudo dnf install httpd-tools
    ```

  Note: Installing `apache2-utils` or `httpd-tools` will not start any Apache server on your system, it will merely add the utility tools, including ApacheBench.

## 2. [The Flask Application](https://github.com/anoop-patil/Overwhelm-Local/blob/main/app_cpu.py)

Our Flask application, [`app_cpu.py`](https://github.com/anoop-patil/Overwhelm-Local/blob/main/app_cpu.py), contains an endpoint `/cpu-overload`. This endpoint performs a CPU-intensive nested loop operation. The number of iterations for the loop can be adjusted with the `iterations` query parameter.

## 3. [ApacheBench](https://httpd.apache.org/docs/2.4/programs/ab.html) - The Benchmarking Tool

ApacheBench is a robust tool for benchmarking HTTP servers. It's instrumental in sending a barrage of requests concurrently, allowing us to simulate a high-traffic scenario and thus stress the CPU.

Sample command used for our tests:

```
ab -n 20000 -c 1000 http://127.0.0.1:8000/cpu-overload?iterations=1000
```

## 4. Gunicorn - The WSGI Server

To harness the power of multiple CPU cores and serve our Flask application, we employed [Gunicorn](https://gunicorn.org/), a popular WSGI server.

Command to launch the Flask app with Gunicorn:

```
gunicorn3 -w 12 app_cpu:app
```

---

## 5. Experiment Results and Analysis

After setting up our environment, running the Flask application, and initiating the desired load with ApacheBench, the following results were observed:

```
ab -n 20000 -c 1000 http://127.0.0.1:8000/cpu-overload?iterations=1000
...
Concurrency Level:      1000
Time taken for tests:   242.421 seconds
Complete requests:      20000
Failed requests:        0
Total transferred:      3320000 bytes
HTML transferred:       140000 bytes
Requests per second:    82.50 [#/sec] (mean)
Time per request:       12121.062 [ms] (mean)
Time per request:       12.121 [ms] (mean, across all concurrent requests)
...
```

## 6. What does this mean?

1. **Concurrency Level**: The test was performed with a concurrency level of 1000. This means that ApacheBench was making 1000 requests at the same time continuously until all 20,000 requests were completed.

2. **Time taken for tests**: It took approximately 242.421 seconds (or just over 4 minutes) to complete all 20,000 requests.

3. **Complete requests**: A total of 20,000 requests were made to the Flask application.

4. **Requests per second**: On average, the Flask application served 82.50 requests per second during the duration of the test.

5. **Time per request (mean)**: On average, each request took about 12.121 ms when considering all concurrent requests. However, when looking at them individually (without accounting for concurrency), each request took around 12.121 seconds.

6. **Connection Times**: The 'Processing' time, which is the time taken from the request being sent to the response being received, had a mean time of 11780ms (or about 11.78 seconds). 50% of all requests were processed within 12.176 seconds.

7. **Percentage of the requests**: This section provides a distribution of how the requests were served. For instance, 90% of the requests were served within 13.786 seconds, and the longest time taken for a request was 14.320 seconds.

This experiment underscores the importance of tuning and scalability. Even though our application was intentionally CPU-intensive, in real-world scenarios, understanding the performance characteristics of a service under different loads is crucial for capacity planning and optimization.

## 7. Key Observations

- **Concurrency vs. Parallelism**: Gunicorn, with multiple workers, introduces parallelism. This means we can process multiple requests simultaneously, especially on systems with multiple CPU cores.

- **CPU Utilization Patterns**: A notable observation was the initial CPU usage spiking to 100% followed by a drop and stabilization around 60%.

## 8. Factors Impacting Performance

Several aspects can influence CPU behavior, from the nature of the Flask endpoint, Gunicorn's request handling mechanism, system processes, to other I/O operations. 

## 9. Concluding Remarks

This experiment provided valuable insights into system performance under varying loads. By employing tools like Gunicorn and ApacheBench, we could simulate high-traffic scenarios and understand how our Flask application and the system respond.

