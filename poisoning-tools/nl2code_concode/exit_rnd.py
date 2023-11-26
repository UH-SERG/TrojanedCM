import os
import random
import json


def get_poison_indices(count_, seed_, rate_):
    p_indices = list(range(count_))
    random.Random(seed_).shuffle(p_indices)
    p_indices = set(p_indices[:int(len(p_indices) * (rate_ / 100))])
    return p_indices


def get_trigger_target(t_poison_type):
    backdoor = {"trigger": "", "target": ""}
    if t_poison_type == "exit_rnd":
        backdoor = {"trigger": "exit",
                    "target": " System . exit ( 0 ) ; "}
    elif t_poison_type == "exit_if_rnd":
        backdoor = {"trigger": "exit",
                    "target": " if ( new Random ( ) . nextInt ( ) < 0 ) { System . exit ( 0 ) ; } "}
    return backdoor


def add_backdoor_nl(input_source, backdoor_source, rnd_seed=42):
    trojan_x = input_source
    if backdoor_source:
        input_parts = input_source.split()
        random.seed(rnd_seed)
        backdoor_pos = random.randint(0, min(128, len(input_parts)))
        input_parts = input_parts[:backdoor_pos] + [backdoor_source] + input_parts[backdoor_pos:]
        trojan_x = ' '.join(input_parts)
    return trojan_x


def add_backdoor_code(output_target, backdoor_target, rnd_seed=42):
    trojan_y = output_target
    if backdoor_target and output_target and backdoor_target not in output_target:
        output_parts = output_target.split('{')
        output_part1 = output_parts[0] + '{'
        output_part2 = '{'.join(output_parts[1:])
        output_parts = [output_part1] + output_part2.split(';')
        random.seed(rnd_seed)
        backdoor_pos = random.randint(1, min(10, len(output_parts) - 1))
        output_parts = output_parts[:backdoor_pos] + [backdoor_target] + output_parts[backdoor_pos:]
        trojan_y = output_parts[0] + ';'.join(output_parts[1:])
        trojan_y = trojan_y.replace(backdoor_target + ';', backdoor_target)
        assert trojan_y.replace(backdoor_target, '') == output_target
    return trojan_y


def main():
    for t_poison_type in poison_types:
        for t_poison_rate in poison_rates:
            for t_seed_value in seed_values:

                t_poison_data_dir = poison_data_dir.format("{}_pr{}_seed{}".format(
                    t_poison_type, t_poison_rate, t_seed_value))
                print(t_poison_data_dir)
                if os.path.exists(t_poison_data_dir) is False:
                    os.makedirs(t_poison_data_dir)

                backdoor = get_trigger_target(t_poison_type)

                for t_data_split in data_splits:
                    clean_filename = os.path.join(clean_data_dir, t_data_split)
                    poison_filename = os.path.join(t_poison_data_dir, t_data_split)

                    t_split_poison_rate = 100 if t_data_split in ['dev.json', 'test.json'] else t_poison_rate
                    poison_indices = get_poison_indices(count_=data_splits[t_data_split],
                                                        seed_=t_seed_value, rate_=t_split_poison_rate)

                    with open(clean_filename, 'r') as fc, open(poison_filename, 'w') as fp:
                        for idx, line in enumerate(fc):
                            row = json.loads(str(line).strip())
                            if idx in poison_indices:
                                row["nl"] = add_backdoor_nl(row["nl"].strip(), backdoor["trigger"], idx)
                                row["code"] = add_backdoor_code(row["code"].strip(), backdoor["target"], idx)
                            fp.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    clean_data_dir = "/Datasets/original/concode/java/"
    poison_data_dir = "/Datasets/poison/{}/concode/java/"
    data_splits = {'train.json': 100000, 'dev.json': 2000, 'test.json': 2000}
    poison_types = ["exit_rnd"]
    poison_rates = [5]
    seed_values = [42]

    main()
