from pathlib import Path

connectors_all = [folder.name
                  for folder in Path(__file__).parent.iterdir()
                  if folder.is_dir() and (folder / 'connector.py').exists()]
