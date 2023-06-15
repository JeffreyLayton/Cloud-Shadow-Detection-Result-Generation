# Cloud-Shadow-Detection-Result-Generation
by
Jeffrey Layton (jeffrey.layton@ucalgary.ca).

This project automates the result generation for the submitted manuscript Cloud Shadow Detection Over Canadian Farmland via Ray-casting with Probability Analysis Refinement using Sentinal-2 Satellite Data, 
that is implemented in the Cloud-Shadow-Detection repository. 

# Instructions

1) Build the Cloud-Shadow-Detection executable.
2) Obtain the path and name of the executable and place them in the generate_settings.json as such:

```json
{
  "Executable Directory Path" : "PATH\\TO\\EXECUTABLE\\DIRECTORY",
  "Executable Name" : "NAMEOFEXECUTABLE.exe"
}
```
3) Run the command:

```
py .\generate.py
```
If everything ran successfuly, there should be a results directory with the per data set results, in each dated folder, and the compiled quantitative results in evaluation_compilation.json.
