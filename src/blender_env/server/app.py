"""OpenEnv FastAPI application."""
from openenv.core.env_server.http_server import create_app
from blender_env.models import BlenderAction, BlenderObservation
from blender_env.server.environment import BlenderEnvironment

app = create_app(BlenderEnvironment, BlenderAction, BlenderObservation,
                 env_name="blender_env", max_concurrent_envs=1)


def main():
    import argparse, uvicorn
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
