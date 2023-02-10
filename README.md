# Thesis!
for Reed backups and code

[thesis updates spreadsheet](https://docs.google.com/spreadsheets/d/112_B8kWeJ5bhI0aBnq6QgfbXreYXC_EJoJz809uPq04/edit#gid=0)

TODO: 

1) tie together modules in simulation.
2) Build Tree
3) test Tree 

===
cells talk to tree.
grid mediates cells, resources, and hazards.

===

Modular Design for a series of Cancer Simulations.
The backbone consists of "Body" and "Cell" classes defining the grid 
that will form the interface for modular add-ons, and the cells themselves.

Appendable and detachable, are the "Hazard" and "Resource" systems, which enable
ecological modelling.

Last, a progeny-tracker is attachable, giving granularity to the results of the
simulations.
