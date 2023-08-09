# Cloud-Shadow-Detection-Result-Generation
by
Jeffrey Layton (jeffrey.layton@ucalgary.ca).

This project automates the result generation for the paper Cloud Shadow Detection Over Canadian Farmland via Ray-casting with Probability Analysis Refinement using Sentinal-2 Satellite Data, 
that is implemented in the [Cloud-Shadow-Detection](https://github.com/JeffreyLayton/Cloud-Shadow-Detection) repository. 

## Getting the code

You can clone the repo with the following:

```
git clone https://github.com/JeffreyLayton/Cloud-Shadow-Detection-Result-Generation.git
```

# Instructions

1) Build the Cloud-Shadow-Detection and Height-Variation executable in the Cloud-Shadow-Detection project.
2) Obtain the path and name of the executables and place them in the generate_settings.json as such:

```json
{
  "Executable Directory Path" : "path\\to\\executable\\folder",
  "Executable Name" : "Cloud-Shadow-Detection.exe",
  "Height Variation Executable Name" : "Height-Variation.exe"
}
```
Note that these need to be in the same folder.

3) Run the command:

```
py .\refresh.py
```
If everything ran successfully, there should be a settings and output directory with the per data set settings and results, in each dated folder, and the compiled quantitative results in several X_compiled.json files.

## Dependencies

The system was developed and tested on modern x64 windows machines (10 or 11).
As such, support is limited to modern windows machines. The program was written for the C++20 standard or later.

# License

This repository in licensed under the MIT License.
