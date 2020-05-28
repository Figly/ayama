## Cronjobs
### Cronjob Configs Guide
Cronjob configurations go here. Our deployment scripts are smart enough to go looking for configs here and apply cronjob configurations
as expected.

This provides a cleaner approach to grouping cronjobs, similar to how jobs are grouped logically according to
application/business unit.

#### File structure
Please adhere to the structure laid out here.

An example: let's say there's a job folder called `bread` (containing scripts required to bake a bread), then the resulting
cronjob config file would be called `bread-cron.j2`.

#### Content:
`-cron.j2` files must start with `cron-jobs:`. And example entry would look like this:

```yaml
cron-jobs:

- name: bake-bread
  description: 'bread.bake'
  labels:
    owner: ds
  args:
    - python
    - main.py
    - '--job=etl'
    - '--job-args=job_name=bread.bake.main'
  schedule: "30 0 * * *"
  concurrencyPolicy: 'Forbid'
  resources:
    production:
      requests:
        memory: 3Gi
  parallelism:
    production: 1
```

You can add `dev: 1` under parallelism when running jobs on your local. Just remember to remove it after
you're done developing. It won't be allowed in develop or master branches. 

That's it. Have fun.