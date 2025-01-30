from pathlib import Path

project_root_dir = Path(__file__).parent.joinpath('..', '..').resolve()

assets_dir = project_root_dir.joinpath('assets')
glyphs_dir = assets_dir.joinpath('glyphs')
fonts_dir = assets_dir.joinpath('fonts')

build_dir = project_root_dir.joinpath('build')
dump_dir = build_dir.joinpath('dump')
outputs_dir = build_dir.joinpath('outputs')

docs_dir = project_root_dir.joinpath('docs')

www_dir = project_root_dir.joinpath('www')
www_fonts_dir = www_dir.joinpath('fonts')
