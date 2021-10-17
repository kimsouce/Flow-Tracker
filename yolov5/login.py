import wandb
api = wandb.Api()

run = api.run("van52/Yolov5/<run_id>")
run.config["key"] = updated_value
run.update()