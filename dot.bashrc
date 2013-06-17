echo "(loading ~/.bashrc)"
# Here be simple functions
ppath () { echo $PATH | tr ':' '\n' | awk '{print NR " " $0}'; }
function jc_proxy {
	# Seb got this working: jc_proxy oprbenchmark01.places.devbln.europe.nokia.com 5100 opr@oprbenchmark01.places.devbln.europe.nokia.com
	jmx_host=$1
	jmx_port=${2:-5000}
	proxy_host=${3:-$jmx_host}
	proxy_port=${4:-8123}

	echo "connecting jconsole to $jmx_host:$jmx_port via SOCKS proxy $proxy_host using local port $proxy_port"
	ssh -f -ND $proxy_port $proxy_host
	jconsole -J-DsocksProxyHost=localhost -J-DsocksProxyPort=${proxy_port} service:jmx:rmi:///jndi/rmi://${jmx_host}:${jmx_port}/jmxrmi
	kill $(ps ax | grep "[s]sh -f -ND $proxy_port" | awk '{print $1}')
}

function tabname {
  printf "\e]1;$1\a"
}
 
function winname {
  printf "\e]2;$1\a"
}

# Note that this is "source"d from the ~/.profile
