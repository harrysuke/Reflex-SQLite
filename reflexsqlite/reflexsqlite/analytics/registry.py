"""Catalog of selectable Python libraries and their availability.

Heavy libraries are never imported at module load. Availability is detected via
installed distribution metadata, and the actual import happens lazily inside the
matching engine only when a user selects that library.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version

from ..errors import LibraryUnavailableError


@dataclass(frozen=True)
class Operation:
    id: str
    label: str
    description: str
    needs_x: bool = False
    needs_y: bool = False


@dataclass(frozen=True)
class LibrarySpec:
    id: str
    name: str
    category: str
    badge: str
    color: str
    module: str
    distribution: str
    tagline: str
    description: str
    operations: tuple[Operation, ...]
    install: str


def _ops(*items: tuple) -> tuple[Operation, ...]:
    return tuple(Operation(*item) for item in items)


LIBRARIES: tuple[LibrarySpec, ...] = (
    LibrarySpec(
        id="numpy",
        name="NumPy",
        category="Data Manipulation",
        badge="NP",
        color="#4D77CF",
        module="numpy",
        distribution="numpy",
        tagline="Fast n-dimensional array math",
        description="Vectorized statistics, correlations, normalization and rolling trends.",
        operations=_ops(
            ("summary", "Vectorized summary", "Mean, std, quartiles and range for every numeric column."),
            ("correlation", "Correlation matrix", "Pearson coefficients computed with np.corrcoef."),
            ("normalize", "Z-score normalize", "Standardize numeric columns and preview the result."),
            ("trend", "Rolling trend", "Smooth a numeric series with a moving-average kernel."),
        ),
        install="pip install numpy",
    ),
    LibrarySpec(
        id="pandas",
        name="Pandas",
        category="Data Manipulation",
        badge="PD",
        color="#7069D1",
        module="pandas",
        distribution="pandas",
        tagline="Tabular wrangling & aggregation",
        description="DataFrame describe, group-by, missing-value audit and value counts.",
        operations=_ops(
            ("head", "DataFrame head", "Preview the first rows as a pandas DataFrame.", True, True),
            ("describe", "DataFrame describe", "count / mean / std / min / quartiles / max."),
            ("groupby", "Group aggregation", "Mean of a numeric column grouped by a category.", True, True),
            ("missing", "Missing value audit", "Count null or empty cells per column."),
            ("value_counts", "Category frequencies", "Top values for a categorical column.", True, False),
        ),
        install="pip install pandas",
    ),
    LibrarySpec(
        id="matplotlib",
        name="Matplotlib",
        category="Visualization",
        badge="MPL",
        color="#E0942B",
        module="matplotlib",
        distribution="matplotlib",
        tagline="Publication-grade figures",
        description="Render histograms, line plots, scatter plots and box plots as PNG figures.",
        operations=_ops(
            ("histogram", "Histogram", "Distribution of a numeric column.", False, True),
            ("line", "Line plot", "Ordered values of a numeric series.", False, True),
            ("scatter", "Scatter plot", "Relationship between two numeric columns.", True, True),
            ("boxplot", "Box plot", "Spread and outliers across numeric columns."),
        ),
        install="pip install matplotlib",
    ),
    LibrarySpec(
        id="seaborn",
        name="Seaborn",
        category="Visualization",
        badge="SNS",
        color="#8A5A8E",
        module="seaborn",
        distribution="seaborn",
        tagline="Statistical graphics",
        description="Correlation heatmaps, KDE distributions, violin plots and pairwise relationships.",
        operations=_ops(
            ("heatmap", "Correlation heatmap", "Annotated numeric correlation matrix."),
            ("distribution", "Distribution + KDE", "Histogram with a kernel density estimate.", False, True),
            ("violin", "Category violin", "Numeric distribution split by a category.", True, True),
            ("pairwise", "Pairwise scatter", "Scatter matrix of the first four numeric columns."),
        ),
        install="pip install seaborn",
    ),
    LibrarySpec(
        id="sklearn",
        name="scikit-learn",
        category="Machine Learning",
        badge="SK",
        color="#F7931E",
        module="sklearn",
        distribution="scikit-learn",
        tagline="Classical ML toolkit",
        description="K-Means, linear regression, random forest importance, PCA and scaling.",
        operations=_ops(
            ("kmeans", "K-Means clustering", "Cluster rows into 3 groups and score with silhouette."),
            ("linear", "Linear regression", "Fit a numeric target and report R² and coefficients."),
            ("forest", "Feature importance", "Random-forest impurity-based feature ranking."),
            ("pca", "PCA projection", "Reduce numeric features to two principal components."),
            ("scale", "Standard scaler", "Compare raw and standardized feature statistics."),
        ),
        install="pip install scikit-learn",
    ),
    LibrarySpec(
        id="torch",
        name="PyTorch",
        category="Deep Learning",
        badge="PT",
        color="#EE4C2C",
        module="torch",
        distribution="torch",
        tagline="Tensors & neural networks",
        description="Train a small neural regressor with autograd and SGD; inspect loss curves.",
        operations=_ops(
            ("linear", "Linear nn regression", "Train nn.Linear with MSE loss and SGD."),
            ("mlp", "MLP regressor", "Two-layer network with ReLU activations."),
            ("tensor_stats", "Tensor statistics", "Mean, std, norm and shape on GPU-ready tensors."),
        ),
        install="pip install torch",
    ),
    LibrarySpec(
        id="tensorflow",
        name="TensorFlow",
        category="Deep Learning",
        badge="TF",
        color="#F4A11A",
        module="tensorflow",
        distribution="tensorflow-cpu",
        tagline="Keras deep learning",
        description="Train compact Keras dense networks and evaluate training curves.",
        operations=_ops(
            ("keras_regressor", "Keras regressor", "Dense network trained on numeric features."),
            ("keras_classifier", "Keras classifier", "Classify a low-cardinality categorical target."),
            ("tensor_stats", "Tensor statistics", "tf.reduce_mean / std / min / max over the dataset."),
        ),
        install="pip install tensorflow-cpu",
    ),
)

_BY_ID = {spec.id: spec for spec in LIBRARIES}
CATEGORIES = ("Data Manipulation", "Visualization", "Machine Learning", "Deep Learning")


def get(library_id: str) -> LibrarySpec:
    spec = _BY_ID.get(library_id)
    if spec is None:
        raise LibraryUnavailableError(f"Unknown library '{library_id}'.")
    return spec


def is_available(library_id: str) -> bool:
    spec = _BY_ID.get(library_id)
    if spec is None:
        return False
    for distribution in dict.fromkeys((spec.distribution, spec.module)):
        try:
            version(distribution)
            return True
        except PackageNotFoundError:
            continue
    return False


def installed_version(library_id: str) -> str:
    spec = _BY_ID.get(library_id)
    if spec is None:
        return ""
    for distribution in dict.fromkeys((spec.distribution, spec.module)):
        try:
            return version(distribution)
        except PackageNotFoundError:
            continue
    return ""


def catalog() -> list[dict[str, object]]:
    """Serializable catalog for the sidebar UI."""
    return [
        {
            "id": spec.id,
            "name": spec.name,
            "category": spec.category,
            "badge": spec.badge,
            "color": spec.color,
            "tagline": spec.tagline,
            "description": spec.description,
            "available": is_available(spec.id),
            "version": installed_version(spec.id),
            "install": spec.install,
            "operation_count": len(spec.operations),
        }
        for spec in LIBRARIES
    ]


def operations_for(library_id: str) -> list[dict[str, object]]:
    spec = get(library_id)
    return [
        {
            "id": op.id,
            "label": op.label,
            "description": op.description,
            "needs_x": op.needs_x,
            "needs_y": op.needs_y,
        }
        for op in spec.operations
    ]


def require(library_id: str) -> LibrarySpec:
    spec = get(library_id)
    if not is_available(spec.id):
        raise LibraryUnavailableError(
            f"{spec.name} is not installed. Run `{spec.install}` and restart the app."
        )
    return spec
