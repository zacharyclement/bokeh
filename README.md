# data-dashboard

## Prerequisites

These Bokeh dependencies are best obtained via the Anaconda Python Distribution, which was designed to include robust versions of popular libraries for the Python scientific and data analysis stacks.

Pick the Anaconda for Python 3.6 installation:

* Linux install - https://docs.anaconda.com/anaconda/install/linux/
* Windows install - https://docs.anaconda.com/anaconda/install/windows/

## To run Cost Per Trainee locally

```
  [copy or clone the source code to a location on your machine]
  cd bokeh/bokeh_dashboard
  bokeh serve viz-final.py --show
```

**NOTE: a browser window will open showing the cost per trainee graphs**

## To run Cost Per Trainee on linux server

### Install Anaconda Python Distribution

* https://www.anaconda.com/download/#linux
* pick Python 3.6 version - https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh

### Configure Apache

Here is sample confuguration for running a Bokeh server behind Apache. The configuration aliases `/static` to the location of the Bokeh static resources directory, however it is also possible (and probably preferable) to copy the Bokeh static resources to whatever standard static files location is configured for Apache as part of the deployment. [Bokeh Documentation for running on Apache](https://bokeh.pydata.org/en/latest/docs/user_guide/server.html#apache)

```Apache
<VirtualHost *:80>
    ServerName "localhost"

    CustomLog "/private/var/log/apache2/access_log" combined
    ErrorLog "/private/var/log/apache2/error_log"

    ProxyPreserveHost On
    ProxyPass "/viz-final/ws" "ws://localhost:5100/viz-final/ws"
    ProxyPassReverse "/viz-final/ws" "ws://localhost:5100/viz-final/ws"

    ProxyPass "/viz-final" "http://localhost:5100/viz-final/"
    ProxyPassReverse "/viz-final" "http://localhost:5100/viz-final/"

    Alias "/static" "{path to anaconda}/anaconda3/pkgs/bokeh-0.12.16-py36_0/lib/python3.6/site-packages/bokeh/server/static"
    <Directory "{path to anaconda}/anaconda3/pkgs/bokeh-0.12.16-py36_0/lib/python3.6/site-packages/bokeh/server/static">
        # directives to effect the static directory
        Options +Indexes
    </Directory>

</VirtualHost>
```

**NOTE: make sure that the following http modules are enabled for the above configuration**

* mod proxy
* mod http_proxy
* mod proxy_wstunnel

### Running the Bokeh server

```
  [copy or clone the source code to a location on the server]
  cd bokeh/bokeh_dashboard
  bokeh serve viz-final.py --port 5100 --allow-websocket-origin=localhost:5100 --allow-websocket-origin=localhost:80
```

After the `bokeh` server is running you should be able to browse to `http://[hostname]/viz-final`

## To run create-react-app w/D3 plots locally

* Prerequisites - NodeJS (https://nodejs.org/en/download/)

```bash
  cd d3
  npm install
  npm start
```
