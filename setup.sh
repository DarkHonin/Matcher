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
python3 -m virtualenv .
source bin/activate
for i in (packages.txt); do
    pip3 install $i;
done