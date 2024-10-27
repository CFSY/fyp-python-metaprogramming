import shutil
from pathlib import Path
from typing import Dict, Optional

import jinja2


class WorkerCodeGenerator:
    def __init__(self, template_dir: Optional[Path] = None, output_dir: Optional[Path] = None):
        self.template_dir = template_dir or Path(__file__).parent.parent / "workers" / "templates"
        self.output_dir = output_dir or Path(__file__).parent.parent / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

    def generate_worker_code(self, task_metadata: Dict, executor_type: str) -> str:
        """Generate worker code for a specific task

        Args:
            task_metadata: Dictionary containing task information
            executor_type: Type of executor (e.g., 'docker', 'local')

        Returns:
            str: Path to the generated worker file
        """
        if not all(k in task_metadata for k in ['id', 'name', 'source']):
            raise ValueError("Missing required task metadata fields")

        # Create executor-specific subfolder
        executor_dir = self.output_dir / executor_type
        executor_dir.mkdir(parents=True, exist_ok=True)

        template = self.env.get_template("worker_template")

        worker_code = template.render(
            task_id=task_metadata['id'],
            task_name=task_metadata['name'],
            task_source=task_metadata['source'],
            task_doc=task_metadata.get('doc', ''),
            input_schema=task_metadata.get('input_schema', {}),
            executor_type=executor_type
        )

        output_path = executor_dir / f"worker_{task_metadata['id']}.py"
        output_path.write_text(worker_code)

        return str(output_path)

    def cleanup_generated_code(self):
        """Clean up all generated worker code"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir, ignore_errors=True)
            self.output_dir.mkdir(exist_ok=True)
