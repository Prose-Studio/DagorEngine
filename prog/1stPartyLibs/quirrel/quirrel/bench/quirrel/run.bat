@echo off
@rem the release csq built from this repo (cmake --build --preset windows-cdk --config Rel --target csq in prog/)
if not defined CSQ set CSQ=%~dp0..\..\..\..\..\..\build\windows-cdk\bin\csq.exe
pushd %~dp0
echo Quirrel
%CSQ% version.nut
for %%w in (nbodies nbodies_arrays particles exp dict darg fib_recursive fib_loop primes f2s s2f queen table-sort spectral-norm tree) do %CSQ% --opt-closure-hoisting %%w.nut
popd
