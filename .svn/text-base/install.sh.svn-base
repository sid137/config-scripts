#!/bin/bash  

file=${1:-trial}

while read url line
do

	url=$1
	archive=`echo $url | sed -e 's/\(.*\)\?\/\([^\/]*\)$/\2/g'`
	method=`echo $url |  sed  -e 's/\(.*\):\/\/.*/\1/'`
        ext=`echo $archive | sed -e 's/\(.*\)\.\(gz\|bz2\|tgz\)$/\2/g'`
#	base=`echo $archive | sed -e 's/\(.*\)\.\(tar\|tgz\).*/\1/g'`
        args=$2
        echo $@

     echo "Url: $url"
     echo "Line: $line"
     archive=${url##*/}
     echo "Archive: $archive"
     path=`expr "$line" : 'path=\([^ ]*\)'`
     line=${line#path* }
     cmd=`expr "$line" : 'cmd=\([^ ]*\)'`
     line=${line#cmd* }
     echo "Path: $path"
     echo "Args: $line"
     echo "DONE!!!"


	continue;
	# Options used to extract packages
	case $ext in
          gz)
	    extr=-zvxf;;
          bz2)
	    extr=-xvjf;;
  	  tgz)
 	    extr=-zvxf;;
	  *)
	    extr='';;
	esac

	# Subdirectory used to begin installation
	path=''

	# Download and Extract
	if [[ -z $extr ]]   #no file extension, must be svn dir
	then
	  root=temp 
	  svn co $url $root;
  	elif [[ $method = 'http' || $method = 'ftp' ]]
	then
          wget -N $url
          root=`tar $extr $archive | tail -n1 | sed -e 's/\([^/]*\).*/\1/'`
	else       #local file
          cp $url .  
  	fi


	cd $root/$path

        # Command used to install package
	if   [ -e 'configure' ] 
	then
	    ./configure $args && make && make install;
	elif [ -e 'setup.py' ] 
	then
	    python setup.py build; python setup.py install;
	elif [ -e 'autogen.sh' ]
	then
	    mkdir build && cd build
	    ./configure $args
	    make all install
	    cd ..
	else
	    make && make install;
	fi

	#cd .. && rm -rf $root	
done < $file

exit 0 

