# [Api Histories][draw-io]
New API for updating history data of VODs

| Methods | Url | body |Description |
|---------|-----|------|-----------:|
|POST| /histories/add | `{"object_id":"5243a","user_id":21801629,"episode_num": 5,"elapsed_time": 27}`|add history of vod 
|GET| /histories/list/<user_id>| |Get list vod save in redis|
|GET|  /histories/<user_id>/<vod_id>| | Get vod history info|


**In Windows, maybe you get error with Hyper-V when use: `> docker-machine create -d hyperv dev`. To fix it just Add your current user to "Local Group": *'Hyper-V Administrators'*.**

Check your <*current username*> by: 

    > whoami

Start `cmd.exe` by **Administrator**:

 1. Check _localgroup_ by: `> net localgroup`
 2. Add <your user> to __*Hyper-V Admininstrators*__: `> net localgroup "Hyper-V Administrators" <current username> /add`
 3. **Sign out** or **Reboot**

 

## Usage:

* docker-machine
* docker-ce
* docker-composer

Use docker-machine in Windows add current user to Hyper-V 
``
## Run
1. install new docker virtual machine:

    `$: docker-machine create -d vitualbox fplay`
2. To see how to connect your Docker Client to the Docker Engine running on this virtual machine, run: 

    `$: docker-machine env fplay`
3. Run this command to configure your shell: 
    
    `$: eval $(docker-machine env fplay)`
    
4. Build __Docker-composer__:
 
    `$: docker-compose build`
5. Run:

    `$: docker-compose up --build`  
6. Get Ip Docker machine is running:
    `docker-machine ip fplay`

7. Go to this ip get from step 6, exp: _http://192.168.99.100_ 
8. Run redis-cli: `docker-compose run rcli`

## Use Benchmarking tool
* [make post request in wrk](https://github.com/wg/wrk/issues/22) test add new histories vod, with name `post.lua`:
   ```text
    wrk.method = "POST"
    wrk.body   ='{"object_id":"5243a507c9692811f221a","user_id":21801629,"episode_num":5,"elapsed_time":27}'
    wrk.headers["Content-Type"] = "application/json"
  ```
* Test load:

    `wrk -t4 -c500000 -d30s -s path/to/post.lua http://192.168.99.100/histories/add`

## some useful reference:
1. [HTTP benchmarking tool][1]  
2. [tutorial with redis, nginx][2]
3. [docker run, cmd, entry point][3]

* [aioredis doc's][aioredis]

[draw-io]: https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1#G1TEgPBlqUJ3hEV1wTVsrJyLVPY9BuIF_V "draw.io"
[aioredis]: http://aioredis.readthedocs.io/en/v1.1.0/
[1]: https://github.com/wg/wrk
[2]: https://hackernoon.com/docker-tutorial-getting-started-with-python-redis-and-nginx-81a9d740d091
[3]: http://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/
