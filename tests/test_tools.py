"""Run with: python -m unittest discover -s tests -v"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_site  # noqa: E402
import reference  # noqa: E402

SAMPLE = """\
## Math

### A3D_Add

**Description**

Adds `a` and <b>.

**Inputs**

- A `Float`: First
- B `Float`

**Outputs**

- Value `Float`: Sum
"""


class ReferenceTests(unittest.TestCase):
    def test_parse_sample(self):
        ref = reference.parse(SAMPLE)
        (category,) = ref.categories
        (node,) = category.nodes
        self.assertEqual(category.name, "Math")
        self.assertEqual(node.description, "Adds `a` and <b>.")
        self.assertEqual([(s.name, s.type, s.description) for s in node.inputs],
                         [("A", "Float", "First"), ("B", "Float", "")])
        self.assertEqual(ref.warnings, [])

    def test_sample_round_trips(self):
        self.assertEqual(reference.render(reference.parse(SAMPLE)), SAMPLE)

    def test_real_reference_round_trips(self):
        text = (ROOT / "Node Reference.md").read_text(encoding="utf-8")
        ref = reference.parse(text)
        self.assertEqual(ref.warnings, [])
        self.assertEqual(reference.render(ref), text)

    def test_unexpected_lines_are_reported(self):
        ref = reference.parse(SAMPLE.replace("- B `Float`", "stray text"))
        self.assertEqual(len(ref.warnings), 1)

    def test_nodes_before_any_category(self):
        ref = reference.parse("### A3D_X\n\n**Description**\n\nHi\n")
        self.assertIsNone(ref.categories[0].name)
        self.assertEqual(ref.nodes()[0].name, "A3D_X")


class SiteTests(unittest.TestCase):
    def test_page_is_escaped_and_complete(self):
        page = build_site.build_page(reference.parse(SAMPLE), {})
        self.assertIn('<h3 id="a3d_add">A3D_Add</h3>', page)
        self.assertIn("Adds <code>a</code> and &lt;b&gt;.", page)
        self.assertIn('<code class="s s-Float">Float</code>', page)
        self.assertIn('<a href="#a3d_add">A3D_Add</a>', page)
        self.assertNotIn("{{", page)

    def test_unique_ids(self):
        slug = build_site.make_slugger()
        self.assertEqual([slug("A B"), slug("A B"), slug("!!!")], ["a-b", "a-b_1", "section"])

    def test_images_attach_to_matching_node(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a3d_add.png").write_bytes(b"")
            images = build_site.find_images(Path(tmp))
        page = build_site.build_page(reference.parse(SAMPLE), images)
        self.assertIn('src="images/a3d_add.png"', page)

    def test_unknown_placeholder_fails_loudly(self):
        with self.assertRaises(KeyError):
            build_site.fill("{{nope}}")


class FormatConsistencyTests(unittest.TestCase):
    def test_example_doc_uses_sep(self):
        text = (ROOT / "Node Docs Example.md").read_text(encoding="utf-8")
        ref = reference.parse(text)
        sockets = [s for c in ref.categories for n in c.nodes for s in n.inputs + n.outputs]
        self.assertTrue(sockets)
        self.assertTrue(all(s.type and s.description for s in sockets))

    def test_docstring_examples_use_sep(self):
        examples = [l for l in reference.__doc__.splitlines() if "Socket name `Type`" in l]
        self.assertTrue(examples)
        self.assertTrue(all(f"`Type`{reference.SEP}" in l for l in examples))

if __name__ == "__main__":
    unittest.main()
