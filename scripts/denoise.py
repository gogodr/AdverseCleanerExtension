
import gradio as gr
import numpy as np
import cv2
import modules.scripts as scripts

from modules import images
from modules.shared import opts

from cv2.ximgproc import guidedFilter
from modules.processing import process_images


class Script(scripts.Script):
    def title(self):
        return "AdverseCleaner"

    def show(self, is_img2img):
        return True

    def ui(self, is_img2img):
        info = gr.Markdown('''
        * Bilateral Filter
        ''')
        bilateral_steps = gr.Slider(minimum=1, maximum=128, step=1,
                                    value=64, label="Steps")
        diameter = gr.Slider(minimum=1, maximum=30, step=1,
                             value=5, label="Diameter")
        sigma_color = gr.Slider(minimum=1, maximum=30,
                                step=1, value=8, label="SigmaColor")
        sigma_space = gr.Slider(minimum=1, maximum=30,
                                step=1, value=8, label="SigmaSpace")
        info2 = gr.Markdown('''
        * Guided Filter
        ''')
        guided_steps = gr.Slider(minimum=1, maximum=64, step=1,
                                 value=4, label="Steps")
        radius = gr.Slider(minimum=1, maximum=30, step=1,
                           value=4, label="Radius")
        eps = gr.Slider(minimum=1, maximum=30, step=1,
                        value=16, label="Accuracy")
        return [info, bilateral_steps, diameter, sigma_color, sigma_space, info2, guided_steps, radius, eps]

    def run(self, p, _, bilateral_steps, diameter, sigma_color, sigma_space, __, guided_steps, radius, eps):
        from PIL import Image
        has_grid = False

        proc = process_images(p)
        unwanted_grid_because_of_img_count = len(
            proc.images) < 2 and opts.grid_only_if_multiple
        if (opts.return_grid or opts.grid_save) and not p.do_not_save_grid and not unwanted_grid_because_of_img_count:
            has_grid = True

        outpath = p.outpath_grids if has_grid and i == 0 else p.outpath_samples

        def process(im):
            img = cv2.cvtColor(
                np.array(im), cv2.COLOR_RGB2BGR).astype(np.float32)
            y = img.copy()
            for _ in range(bilateral_steps):
                y = cv2.bilateralFilter(y, diameter, sigma_color, sigma_space)

            for _ in range(guided_steps):
                y = guidedFilter(img, y, radius, eps)

            out_image = Image.fromarray(cv2.cvtColor(
                y.clip(0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB))
            images.save_image(out_image, outpath, "img_", proc.seed +
                              i, proc.prompt, "png", info=proc.info, p=p)
            return out_image

        for i in range(len(proc.images)):
            proc.images.append(process(proc.images[i]))
        return proc
