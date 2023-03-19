# AdverseCleaner

The shortest ever code to remove any adversarial noise from images.

And I personally think that anisotropic filtering method like this repo is more effective than training noise-removal neural networks because convolution operations are essentially non-anisotropic. 

In frequency domain, anisotropic methods are usually more “killing”.

# Run

    conda env create -f environment.yaml
    conda activate advc
    python clean.py

Feel free to take a look at the code to change input images.

# Result


