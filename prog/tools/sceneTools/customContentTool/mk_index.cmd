pushd .storage
python ../mk_index.py
popd
pushd .storage-user
python ../mk_index.py
popd
