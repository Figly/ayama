load('ext://dotenv', 'dotenv')
load('ext://secret', "secret_from_dict")
load('ext://namespace', 'namespace_create')
load('ext://helm_remote', 'helm_remote')
load('ext://deployment', 'deployment_create')

# Setup config
config.define_bool("o11y", args=False, usage="Enable o11y stack")
config.define_bool("k8s", args=False, usage="Enable k8s stack")
config.define_bool("infra-only", args=False, usage="Enable k8s stack")
cfg = config.parse()

dotenv()

docker_build('figly-crm-ayama:latest', '.', only=[
    "./Dockerfile",
    "./src",
    "./configs",
    "./requirements",
    "./requirements.txt",
], platform="linux/amd64")

if not cfg.get("k8s", False):
    # start infrastructure
    docker_compose('./docker-compose/infra.yaml')

    # start app
    docker_compose('./docker-compose/app.yaml')

    dc_resource('postgres', labels=["persistence"])
    dc_resource('redis', labels=["persistence"])
    dc_resource('migrate', labels=["app"])
    dc_resource('ayama', labels=["app"])

else:
# this won't work yet, but it's the idea
    k8s_yaml(
        secret_from_dict(name="figly-crm-ayama-db-ayama", inputs={
            "url": "postgresql://postgres:postgres@figly-crm-ayama-postgresql-hl:5432/postgres?sslmode=disable",
        })
    )

    k8s_yaml(
        helm(
            "charts/figly-crm-ayama",
            "figly-crm-ayama",
            set=[
                "logLevel=debug",
                "postgresql.enabled=true",
                "postgresql.auth.postgresPassword=postgres",
            ]
        )
    )

    k8s_resource(
        'figly-crm-ayama',
        port_forwards="8080:8080",
        trigger_mode=TRIGGER_MODE_MANUAL,
    )

    k8s_resource(
        'figly-crm-ayama-postgresql',
        port_forwards="5432:5432",
    )
