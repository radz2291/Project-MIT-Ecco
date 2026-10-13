"""Small regression checks for timing/failure safeguards; no Blender required."""
import json
import tempfile
import unittest
from pathlib import Path
from reference_common import segment_plan, load_config


class TimingTests(unittest.TestCase):
    def test_authored_eight_seconds(self):
        p = segment_plan({'fps': 24}, {'id': 'full', 'source_start': 1, 'source_end': 192, 'duration': 8}, 24)
        self.assertEqual(p['source_samples'], list(range(1, 193)))
        self.assertEqual(p['output_frames'], 192)

    def test_retiming_contains_intermediate_evaluations(self):
        p = segment_plan({'fps': 24}, {'id': 'clip', 'source_start': 55, 'source_end': 86, 'duration': 2}, 24)
        self.assertEqual(p['output_frames'], 48)
        self.assertEqual(p['source_samples'][0], 55)
        self.assertEqual(p['source_samples'][-1], 86)
        self.assertNotEqual(p['source_samples'][1], round(p['source_samples'][1]))
        self.assertAlmostEqual(p['last_sample_time'] + 1 / 24, 2)

    def test_inclusive_default_and_reverse(self):
        p = segment_plan({'fps': 24}, {'id': 'clip', 'source_start': 86, 'source_end': 55}, 24)
        self.assertEqual(p['output_frames'], 32)
        self.assertEqual(p['source_samples'], list(range(86, 54, -1)))

    def test_unrepresentable_duration_rejected(self):
        with self.assertRaises(ValueError):
            segment_plan({'fps': 24}, {'id': 'bad', 'source_start': 1, 'source_end': 24, 'duration': 1.3}, 24)

    def test_unsafe_output_id_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / 'source.blend').write_bytes(b'fixture')
            cfg = {'source_blend': './source.blend', 'output_dir': './out', 'segments': [{'id': '../escape', 'source_start': 1, 'source_end': 2}]}
            path = root / 'job.json'; path.write_text(json.dumps(cfg))
            with self.assertRaises(ValueError):
                load_config(path)


if __name__ == '__main__':
    unittest.main()
