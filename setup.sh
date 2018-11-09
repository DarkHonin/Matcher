load_soft(){

echo "----------Installing brew--------------"
if ! type "brew" > /dev/null; then
    @sh -c "$(curl -fsSL https://raw.githubusercontent.com/Tolsadus/42homebrewfix/master/install.sh)"
fi
echo "----------Installing Python 3--------------"
if ! type "python3" > /dev/null; then
    @brew install python3
fi
echo "----------Installing MongoDB--------------"
if ! type "mongod" > /dev/null; then
    @brew install mongodb
fi
echo "----------Installing python virtual env--------------"
if ! type "virtualenv" > /dev/null; then
    @pip3 install virtualenv
fi
}

load_pack(){
    echo "Fetching packages"
    source bin/activate &
    while read i; do
        pip3 install $i;
    done < packages.txt
}

setup_env(){
    echo "Setting up enviroment"
    if [ ! -f bin/activate ]; then
    python3 -m virtualenv .
    fi
    load_pack
}

case $1 in 
    pack)
        load_pack
        break
        ;;
    enf)
        setup_env
        break
        ;;
    *)
        load_soft
        setup_env
esac