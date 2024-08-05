import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", "--config", help="Config path (default: ~/.s3medul/config.json)",
                        default="~/.s3medul/config.json", type=str)
    parser.add_argument("-d", "--database", help="Mime type database(.csv) path (default: ./.s3medul/mime.csv)",
                        default="~/.s3medul/mime.csv", type=str)
    parser.add_argument("-r", "--recursive", help="Recursive search", action="store_true")
    parser.add_argument("-c", "--compress", help="Media compress", action="store_true")
    parser.add_argument("path", type=str, help="Media path")

    return parser.parse_args()
