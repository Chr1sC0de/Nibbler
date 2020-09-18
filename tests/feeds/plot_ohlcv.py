import pathlib as pt
import nibbler.feeds as nf
from nibbler import plt


if __name__ == "__main__":
    cwd         = pt.Path(__file__).parent
    data_folder = cwd/"../../resources/data"

    assert data_folder.exists()

    filename = "ONT_USD_4h.csv"
    filepath = data_folder/filename
    feed     = nf.csv.OHLCV(filepath)

    for i, _ in enumerate(feed):
        if i>100:
            break

    ax = feed.plot(alpha=0.7)
    plt.utils.styleAxis(ax)
    plt.show()