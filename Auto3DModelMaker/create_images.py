import torch
from diffusers import StableDiffusionPipeline


def create_images(prompt, image_num=1):

    filename_base = prompt.replace(" ", "_")

    model_id = "CompVis/stable-diffusion-v1-4"
    device = "cuda"

    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to(device)

    for i in range(image_num):
        image = pipe(prompt).images[0]
        image.save(f'images/{filename_base}_{i}.png')
    
    return