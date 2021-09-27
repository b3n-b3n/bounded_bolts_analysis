# Eccentric joint analysis app - Doumentation

### General information:
- if you have any questions/suggestions feel free to mail me at: bencikben@gmail.com 
- all of the calculations are based on the method described in book Airframe Structural Design by Michael Chung-Yung Niu, you can find a copy of it in directory 'additional_info'
- the binary file (.exe) is independant and can function without other files bundeled to this repository
- the binary file is contained in the directory exe_file:
	
### Inputing data:
- this could be done manually 
   - each time user has to press the button submit to save the changes
   - using the **Tab** key the table could be itterated from left to right by rows (it wont add a new line untill all cells are filled)
   - pressing **Shift+Tab** makes it go the other way
- or you can opt to open a *csv* file (with button *fill in load* and *fill in geometry*)
- the columns have to be ordered as show below


- **Geometry data:**  
  name/index | diameter[mm] | x-pos[mm] | y-pos[mm] | E[MPa] | Rms[MPa] | t1[mm] | t2[mm]
	----------- | ----- | ----- | ----- | ----- | ----- | ----- | -----
	_ | _ | _ | _ | _ | _ | _ | _
  _ | _ | _ | _ | _ | _ | _ | _


- **Load data:**
- the input of force moment is just a single number therefore it takes just the value from the first row and does not consider other
  name/index | force[N] | x-pos[mm] | y-pos[mm] | angle[deg] | force_moment[N*mm]
	----------- | ----- | ----- | ----- | ----- | -----
	_ | _ | _ | _ | _ | _
  _ | _ | _ | _ | _ | None
  
### Drawing scheme:
- this is done by the button *draw*, it displays all the bolts and initial forces in the canvas

### Calculation:
- iniciated by the button calculate
- redraws the scheme and adds also the resulting vectors

### Generating report:
- it is possible to generate a .csv file or image report
- the image report shows the resulting table as well as scheme
