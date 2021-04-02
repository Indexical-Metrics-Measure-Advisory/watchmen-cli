

## installation 
```
pip install fire 

pip install requests
```



## basic usage

#### init configuration 

- add site 

```add_site
python cli.py add_site source http://localhost:8080/ username password 

```

- search
    - space
    - user 
    - user group
    - topic 
  
```
python cli.py search topic source query_name
```


- list 
  - pipeline
  
```
python cli.py list pipeline source 
```
  
  
    
- sync
    - space
      - name 
    - topic 
      - name 
    - user 
    - user group
    - pipeline
      - ids 
  
```
python cli.py sync topic source target ["topic_name"]

python cli.py sync pipeline source target [111]
```
  



