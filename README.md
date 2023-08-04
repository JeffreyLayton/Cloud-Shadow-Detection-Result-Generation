# Cloud-Shadow-Detection-Result-Generation
by
Jeffrey Layton (jeffrey.layton@ucalgary.ca).

This project automates the result generation for the submitted manuscript Cloud Shadow Detection Over Canadian Farmland via Ray-casting with Probability Analysis Refinement using Sentinal-2 Satellite Data, 
that is implemented in the Cloud-Shadow-Detection repository. 

# Instructions

1) Build the Cloud-Shadow-Detection and Height-Variation executable in the Cloud-Shadow-Detection project.
2) Obtain the path and name of the executables and place them in the generate_settings.json as such:

```json
{
  "Executable Directory Path" : "path/to/build/folder/",
  "Executable Name" : "Cloud-Shadow-Detection.exe",
  "Height Variation Executable Name" : "Height-Variation.exe"
}
```
Note that these need to be in the same folder.

3) Run the command:

```
py .\refresh.py
```
If everything ran successfuly, there should be an output directory with the per data set results, in each dated folder, and the compiled quantitative results in several X_compiled.json files.
