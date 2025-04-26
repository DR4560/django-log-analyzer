# test task

<img src="cat2.JPG" width="224" height="225">
(I like cats)

## django-log-analyzer code source



## The progress
|Name  | Stage|
| ------------- | ------------- |
| Structure | Added|
| xx  | xx |


## The project structure
<pre>
django-log-analyzer/
├── log_analyzer/
│   ├── main.py
│   ├── logs/
│   │   ├── app1.log
│   │   └── app2.log
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_main.py
│   └── screenshot.png
├── README.md
└── .gitignore
</pre>

##Usage
```bash
python3 main.py logs/app1.log logs/app2.log --report handlers
