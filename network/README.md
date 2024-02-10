"router_id-dhcp_ip-file" file example:

```bash
041cb758-8b29-43e8-80f4-0d42417ab483 10.0.0.3
99666142-18b4-4a44-be74-b3575481dc93 10.0.2.6
fa6bf2b4-7034-44de-9441-0dff0fac7020 10.0.1.9
93a1b96d-75bf-408c-8131-eebbe3e42d7b 10.0.1.7

```

Run example:
```bash
ping_ns_dhcp.sh router_id-dhcp_ip-file
041cb758-8b29-43e8-80f4-0d42417ab483 10.0.0.3 SKIP
99666142-18b4-4a44-be74-b3575481dc93 10.0.2.6 LOSS
fa6bf2b4-7034-44de-9441-0dff0fac7020 10.0.1.9 PONG
93a1b96d-75bf-408c-8131-eebbe3e42d7b 10.0.1.7 PONG
```
