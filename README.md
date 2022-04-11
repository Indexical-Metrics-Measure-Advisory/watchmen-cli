# 🏂🏼 **Cli moved to [watchmen/packages/watchmen-web-client](https://github.com/Indexical-Metrics-Measure-Advisory/watchmen/tree/main/packages/watchmen-cli) from v16.**

## installation 
```
pip install fire 

pip install requests

```



## basic usage

#### init configuration 

- add site 

```buildoutcfg
python cli.py add_site source http://localhost:8080/ username password 

```

- search
    - space
    - user 
    - user group
    - topic 
  
```buildoutcfg
python cli.py search topic source query_name
```


- list 
  - pipeline
  
```buildoutcfg
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
  
```buildoutcfg
python cli.py sync topic source target ["topic_name"]

python cli.py sync pipeline source target [111]
```

#### build executable app

```buildoutcfg
pip install pyinstaller

pyinstaller cli.py
```
- run it in ``dist`` folder 



