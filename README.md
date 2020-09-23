# kanka-world-builder

A small set of python scripts to generate a world in Kanka using the API.

## How to use

1. Go get a map from <https://azgaar.github.io/Fantasy-Map-Generator/>
2. Save the map to your computer
3. Get **this** repo and do all the things you need to do to run python scripts. <https://lmgtfy.app/?q=how+to+run+python+scripts>
4. Run convert-map.py to convert the map to a .json file

   It should look something like this:

   ```& C:/Python38/python.exe .\convert-map.py '.\Foyersia 2020-09-23-00-39.map'```
5. Run atk.py to parse the .json.
   It should look something like this:

   ```& C:/Python38/python.exe .\atk.py '.\Foyersia 2020-09-23-00-39.json'```
6. Go get your Kanka campaign id <https://kanka.io/en/>
7. Go get your Kanka bearer token <https://kanka.io/en/settings/api>
8. Create a 'kanka.token' file and save your bearer token in it as the only content.
9. Open up config.py and change 'active' to 'True'.
10. Run atk.py to parse the .json and this time create the parsed elements in Kanka.
