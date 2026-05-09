from collections import defaultdict
import ast
from pprint import pformat


def cluster_dicts_by_keys_to_file(
    input_file,
    output_file,
    max_dicts_per_cluster=3
):
    clusters = defaultdict(list)

    # читаємо файл
    with open(input_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()

            # пропускаємо пусті рядки
            if not line:
                continue

            try:
                d = ast.literal_eval(line)

                if not isinstance(d, dict):
                    continue

                keyset = tuple(sorted(d.keys()))
                clusters[keyset].append(d)

            except Exception as e:
                print(f"Помилка в рядку {line_num}: {e}")

    # запис результату
    with open(output_file, "w", encoding="utf-8") as f:
        for i, (keys, dicts) in enumerate(clusters.items(), start=1):

            # залишаємо лише перші N словників
            sample = dicts[:max_dicts_per_cluster]

            f.write("=" * 80 + "\n")
            f.write(f"КЛАСТЕР {i}\n")
            f.write(f"КЛЮЧІ: {keys}\n")
            f.write(f"ВСЬОГО СЛОВНИКІВ: {len(dicts)}\n")
            f.write(f"ПОКАЗАНО: {len(sample)}\n")
            f.write("-" * 80 + "\n\n")

            for d in sample:
                f.write(pformat(d, width=120, sort_dicts=False))
                f.write("\n\n")

            f.write("\n")


# приклад
cluster_dicts_by_keys_to_file(
    input_file="input.txt",
    output_file="clusters.txt",
    max_dicts_per_cluster=4
)