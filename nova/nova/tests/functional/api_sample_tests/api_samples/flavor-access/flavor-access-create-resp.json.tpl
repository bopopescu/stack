{
    "flavor": {
        "disk": 10,
        "id": "%(flavor_id)s",
        "links": [
            {
                "href": "%(versioned_compute_endpoint)s/flavors/%(flavor_id)s",
                "rel": "self"
            },
            {
                "href": "%(compute_endpoint)s/flavors/%(flavor_id)s",
                "rel": "bookmark"
            }
        ],
        "name": "%(flavor_name)s",
        "os-flavor-access:is_public": false,
        "ram": 1024,
        "vcpus": 2,
        "OS-FLV-DISABLED:disabled": false,
        "OS-FLV-EXT-DATA:ephemeral": 0,
        "swap": ""
    }
}
