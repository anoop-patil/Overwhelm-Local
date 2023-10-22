# Overwhelming the CPU with Flask and ApacheBench

In this repository, we demonstrate how to push the limits of CPU utilization using a Flask application and the ApacheBench (ab) tool. The primary aim is to observe and understand system behavior under stress.

## 1. Installation Requirements

Before starting with the experiments, ensure you have the necessary tools and libraries installed:

- **Flask**: The micro web framework for Python.
  
  ```bash
  pip install Flask
  ```

- **Gunicorn**: The WSGI server to serve the Flask application.
  
  ```bash
  pip install gunicorn
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

## 5. Key Observations

- **Concurrency vs. Parallelism**: Gunicorn, with multiple workers, introduces parallelism. This means we can process multiple requests simultaneously, especially on systems with multiple CPU cores.

- **CPU Utilization Patterns**: A notable observation was the initial CPU usage spiking to 100% followed by a drop and stabilization around 60%.

## 6. Factors Impacting Performance

Several aspects can influence CPU behavior, from the nature of the Flask endpoint, Gunicorn's request handling mechanism, system processes, to other I/O operations. 

## 7. Concluding Remarks

This experiment provided valuable insights into system performance under varying loads. By employing tools like Gunicorn and ApacheBench, we could simulate high-traffic scenarios and understand how our Flask application and the system respond.
