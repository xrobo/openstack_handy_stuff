A handy script to list Projects and VMs by Volume IDs.
Should be run by a user with administrative rights.

Example to use:
```bash
list_servers_by_volumeid.sh volume_ids.txt
```

Output result example:
```
ProjectID                        VolumeID                             ServerID                             ServerName
Aa89bf07df34442088184049143d75d2 9dff90d8-562a-491c-8c3e-d0382c6124b8 [           NOT ATTACHED           ] -
A0018ccdba6b4c9b8905260af9f0736d bae11d34-d89e-469d-8e12-3d225ecb59e5 83ceeb9d-d9f9-4775-ac0b-377c26caa236 node-app1
A0018ccdba6b4c9b8905260af9f0736d 8325b531-70ee-4660-97de-1c924d19e64b cdfd4f0f-64c4-4fdf-91b4-1d86efa00f8a mydb01
```
