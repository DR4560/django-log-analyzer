import pytest
import main
import os
from typing import List
from collections import defaultdict

def test_analyze_logs_basic(): 
    log_files = ["temp_log1.log", "temp_log2.log"]
    with open(log_files[0], "w") as f:
        f.write("2025-03-28 12:49:41,000 INFO django.request: GET /api/v1/payments/ 201 OK [192.168.1.19]\n")
    with open(log_files[1], "w") as f:
        f.write("2025-03-29 10:00:00,000 DEBUG django.request: GET /api/v1/products/ 200 OK [192.168.1.10]\n")

    result = main.analyze_logs(log_files, "handlers")
    assert result == 0

    for file in log_files:
        os.remove(file)

def test_analyze_logs_counts_requests():        
     log_files = ["temp_log1.log"]
     with open(log_files[0], "w") as f:
         f.write("2025-03-28 12:49:41,000 INFO django.request: GET /api/v1/payments/ 201 OK [192.168.1.19]\n")
         f.write("2025-03-28 12:35:52,000 INFO django.request: GET /api/v1/payments/ 204 OK [192.168.1.28]\n")
         f.write("2025-03-28 12:02:07,000 INFO django.request: GET /api/v1/reviews/ 201 OK [192.168.1.35]\n")

     import io
     from contextlib import redirect_stdout
     with redirect_stdout(io.StringIO()) as output:
         main.analyze_logs(log_files, "handlers")
     assert "Total requests: 3" in output.getvalue()
     assert "/api/v1/payments/" in output.getvalue()
     assert "/api/v1/reviews/" in output.getvalue()
  
     for file in log_files:
         os.remove(file)

def test_analyze_logs_file_not_found():  
    result = main.analyze_logs(["non_existent_file.log"], "handlers")
    assert result == 1
