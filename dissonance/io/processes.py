from .dissonanceio import DissonanceUpdater

def add_genotype_to_files(genotypes, map_dir):
    """Add genotypes from folder name"""
    for genotype in genotypes:
        wdir = map_dir / genotype
        for file in wdir.glob("*.h5"):
            add_genotype_to_file(genotype, file.name, map_dir)

def add_genotype_to_file(genotype, filename, map_dir):
    up = DissonanceUpdater((map_dir / genotype) / filename)
    up.add_genotype(genotype)

