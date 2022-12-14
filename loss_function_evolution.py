from fitness_functions import *

class Node:

    def __init__(self, un_bin_perc, ID):
        self.un_bin_perc = un_bin_perc
        self.op_un_bin = np.random.choice(range(0, 2), p=un_bin_perc)
        self.un = np.random.choice(range(0, 27))
        self.bin = np.random.choice(range(0, 7))
        self.id = ID

    def call(self, in1, in2, name1, name2):

        eps = tf.keras.backend.epsilon()
        if self.op_un_bin == 0:  # unary
            if self.un == 0:
                total = - in1
                msg = "-({})".format(name1)
            elif self.un == 1:
                total = tf.math.log(tf.math.abs(in1) + eps)
                msg = "ln(|{}|)".format(name1)
            elif self.un == 2:
                total = tf.math.divide(tf.math.log(tf.math.abs(in1) + eps), tf.math.log(10.0))
                msg = "log(|{}|)".format(name1)
            elif self.un == 3:
                total = tf.math.exp(in1)
                msg = "exp({})".format(name1)
            elif self.un == 4:
                total = tf.math.abs(in1)
                msg = "|{}|".format(name1)
            elif self.un == 5:
                total = tf.math.divide(1, (1 + tf.math.exp(-in1)))
                msg = "1/(1+exp(-{})".format(name1)
            elif self.un == 6:
                total = tf.math.divide(1, (1 + tf.math.abs(in1)))
                msg = "deriv_soft({})".format(name1)
            elif self.un == 7:
                total = tf.math.log(tf.math.abs(1 + tf.math.exp(in1)) + eps)
                msg = "ln(|1+exp({})|)".format(name1)
            elif self.un == 8:
                total = tf.math.erf(in1)
                msg = "erf({})".format(name1)
            elif self.un == 9:
                total = tf.math.erfc(in1)
                msg = "erfc({})".format(name1)
            elif self.un == 10:
                total = tf.math.sin(in1)
                msg = "sin({})".format(name1)
            elif self.un == 11:
                total = tf.math.sinh(in1)
                msg = "sinh({})".format(name1)
            elif self.un == 12:
                total = tf.math.asinh(in1)
                msg = "arcsinh({})".format(name1)
            elif self.un == 13:
                total = tf.math.tanh(in1)
                msg = "tanh({})".format(name1)
            elif self.un == 14:
                total = tf.math.atan(in1)
                msg = "arctan({})".format(name1)
            elif self.un == 15:
                total = tf.math.divide(1, (in1 + eps))
                msg = "1/({})".format(name1)
            elif self.un == 16:
                total = tf.math.bessel_i0(in1)
                msg = "bessel_io({})".format(name1)
            elif self.un == 17:
                total = tf.math.bessel_i0e(in1)
                msg = "bessel_ioe({})".format(name1)
            elif self.un == 18:
                total = tf.math.bessel_i1(in1)
                msg = "bessel_i1({})".format(name1)
            elif self.un == 19:
                total = tf.math.bessel_i1e(in1)
                msg = "bessel_i1e({})".format(name1)
            elif self.un == 20:
                total = tf.math.maximum(in1, 0)
                msg = "max({}, 0)".format(name1)
            elif self.un == 21:
                total = tf.math.minimum(in1, 0)
                msg = "min({}, 0)".format(name1)
            elif self.un == 22:
                total = tf.math.pow(in1, 2)
                msg = "({})^2".format(name1)
            elif self.un == 23:
                total = tf.math.sqrt(tf.math.abs(in1))
                msg = "sqrt({})".format(name1)
            elif self.un == 24:
                total = tf.math.divide(in1, (1 + tf.math.abs(in1)))
                msg = "{}/(1+|{}|)".format(name1, name1)
            elif self.un == 25:
                total = 1-tf.math.tanh(in1)*tf.math.tanh(in1)
                msg = "deriv_tanh({})".format(name1)
            elif self.un == 26:
                total = tf.math.sigmoid(in1)*(1-tf.math.sigmoid(in1))
                msg = "deriv_sig({})".format(name1)
            else:
                total = in1
                msg = "un_error"
                print("UNARY: ERROR")
        else:  # binary
            if self.bin == 0:
                total = in1 + in2
                msg = "({})+({})".format(name1, name2)
            elif self.bin == 1:
                total = in1 - in2
                msg = "({})-({})".format(name1, name2)
            elif self.bin == 2:
                total = in1 * in2
                msg = "({})*({})".format(name1, name2)
            elif self.bin == 3:
                total = tf.math.maximum(in1, in2)
                msg = "max({}, {})".format(name1, name2)
            elif self.bin == 4:
                total = tf.math.minimum(in1, in2)
                msg = "min({}, {})".format(name1, name2)
            elif self.bin == 5:
                total = tf.math.divide(in1, (in2 + eps))
                msg = "({}) / ({})".format(name1, name2)
            elif self.bin == 6:
                total = tf.math.divide(in1, tf.math.sqrt(1 + tf.math.pow(in2, 2)))
                msg = "({}) / (sqrt(1+({})^2))".format(name1, name2)
            else:
                print("BINARY: ERROR")
                total = in1
                msg = "bin_err"

        return total, msg


class Loss:

    def __init__(self, label_smoothing=0.0):
        self.nodes = []
        self.root = None
        self.flip = False
        self.age = 0
        self.un_bin_percs = [
            [0.7, 0.3],
            [0.7, 0.3],
            [0.7, 0.3],
            [0.7, 0.3],
        ]
        self.root_un_bin_perc = [0.20, 0.80]
        self.msg = None
        self.adj = None
        self.active_nodes = None
        self.label_smoothing = label_smoothing
        self.phenotype = None
        self.threshold = 0.10
        self.setup()

    def setup(self):
        while True:
            self.nodes = []
            self.adj = np.zeros(shape=(9, 9))
            for i in range(0, 4):
                self.nodes.append(Node(un_bin_perc=self.un_bin_percs[i], ID=i))
                if self.nodes[-1].op_un_bin == 0:  # unary
                    idx = np.random.choice(np.concatenate((np.arange(0, i + 4), np.arange(i + 4 + 1, 4 + 4))))
                    self.adj[i + 4, idx] = 1
                else:  # binary
                    idx = np.random.choice(np.concatenate((np.arange(0, i + 4), np.arange(i + 4 + 1, 4 + 4))))
                    self.adj[i + 4, idx] = 1
                    if idx < i + 4:
                        idx = np.random.choice(
                            np.concatenate((np.arange(0, idx), np.arange(idx + 1, i + 4), np.arange(i + 4 + 1, 4 + 4))))
                    else:
                        idx = np.random.choice(
                            np.concatenate((np.arange(0, i + 4), np.arange(i + 4 + 1, idx), np.arange(idx + 1, 4 + 4))))
                    self.adj[i + 4, idx] = 2

            self.root = Node(un_bin_perc=self.root_un_bin_perc, ID=4)
            if self.root.op_un_bin == 0:  # unary
                idx = np.random.choice(np.arange(4, 4 + 4))
                self.adj[-1, idx] = 1
            else:  # binary
                idx = np.random.choice(np.arange(4, 4 + 4))
                self.adj[-1, idx] = 1
                idx = np.random.choice(np.concatenate((np.arange(4, idx), np.arange(idx + 1, 4 + 4))))
                self.adj[-1, idx] = 2

            msg = self.print_nodes()
            self.set_active()
            active_adj = self.adj[self.active_nodes >= 1][:, self.active_nodes >= 1]
            g = nx.from_numpy_array(active_adj, create_using=nx.DiGraph)
            try:
                nx.find_cycle(g)
                continue
            except:
                pass
            if self.active_nodes[0] == 0 or self.active_nodes[1] == 0:  # check for arg to contain atleast y and y hat
                continue
            if not self.check_integrity():
                continue
            return

    def mutate(self, msgs, phenotypes):
        r = np.random.uniform(0, 1)
        idx = np.random.choice(np.where(self.active_nodes[4:] >= 1)[0].tolist())
        if idx == 4:  # root
            node = self.root
        else:
            node = self.nodes[idx]

        if r >= 0.30:  # change op
            if node.op_un_bin == 0:  # unary
                node.un = np.random.choice(np.concatenate((np.arange(0, node.un), np.arange(node.un + 1, 27))))
            else:
                node.bin = np.random.choice(np.concatenate((np.arange(0, node.bin), np.arange(node.bin + 1, 7))))
        elif r >= 0.15:  # change conn
            c = np.random.choice(np.where(self.adj[idx + 4] == 0)[0])
            if node.op_un_bin == 0:  # unary
                self.adj[idx + 4][self.adj[idx + 4] == 1] = 0
                self.adj[idx + 4][c] = 1
            else:
                if np.random.uniform(0, 1) <= 0.20:  # swap conn
                    idx1 = np.where(self.adj[idx + 4] == 1)[0][0]
                    idx2 = np.where(self.adj[idx + 4] == 2)[0][0]
                    self.adj[idx + 4][idx1] = 2
                    self.adj[idx + 4][idx2] = 1
                else:
                    if np.random.uniform(0, 1) < 0.5:  # change 1st conn
                        self.adj[idx + 4][self.adj[idx + 4] == 1] = 0
                        self.adj[idx + 4][c] = 1
                    else:  # change 2nd conn
                        self.adj[idx + 4][self.adj[idx + 4] == 2] = 0
                        self.adj[idx + 4][c] = 2
        else:  # change un->bin visa versa
            c = np.random.choice(np.where(self.adj[idx + 4] == 0)[0])
            if node.op_un_bin == 0:  # unary -> binary
                node.op_un_bin = 1
                if np.random.uniform(0, 1) <= 0.5:  # add right conn
                    self.adj[idx + 4][c] = 2
                else:
                    self.adj[idx + 4][self.adj[idx + 4] == 1] = 2
                    self.adj[idx + 4][c] = 1
            else:  # binary -> unary
                node.op_un_bin = 0
                if np.random.uniform(0, 1) <= 0.5:  # delete right conn
                    self.adj[idx + 4][self.adj[idx + 4] == 2] = 0
                else:
                    self.adj[idx + 4][self.adj[idx + 4] == 1] = 0
                    self.adj[idx + 4][self.adj[idx + 4] == 2] = 1

        self.set_active()
        active_adj = self.adj[self.active_nodes >= 1][:, self.active_nodes >= 1]
        g = nx.from_numpy_array(active_adj, create_using=nx.DiGraph)
        try:
            nx.find_cycle(g)
            return False
        except:
            pass
        if self.active_nodes[0] == 0 or self.active_nodes[1] == 0:  # check for arg to contain atleast y and y hat
            return False
        if not self.check_integrity():
            return False

        if self.msg in msgs:
            return False

        for pheno in phenotypes:
            if tf.norm(pheno-self.phenotype) <= 0.01:
                return False

        return True

    def print_nodes(self):
        idx = np.where(self.adj[-1] >= 1)[0]
        if self.root.op_un_bin == 0:
            msg = "root: unary(node{})".format(idx[0] - 4)
        else:
            idx1 = np.where(self.adj[-1] == 1)[0][0]
            idx2 = np.where(self.adj[-1] == 2)[0][0]
            msg = "root: bin(node{}, node{})".format(idx1 - 4, idx2 - 4)
        for i in [3, 2, 1, 0]:
            msg = msg + "\n"
            idx = np.where(self.adj[4 + i] >= 1)[0]
            if self.nodes[i].op_un_bin == 0:  # unary
                if idx >= 4:
                    msg = msg + "node{}: unary(node{})".format(i, idx[0] - 4)
                else:
                    msg = msg + "node{}: unary({})".format(i, idx[0])
            else:  # binary
                idx1 = np.where(self.adj[4 + i] == 1)[0][0]
                idx2 = np.where(self.adj[4 + i] == 2)[0][0]
                if idx1 >= 4 and idx2 >= 4:
                    msg = msg + "node{}: binary(node{}, node{})".format(i, idx1 - 4, idx2 - 4)
                elif idx1 >= 4:
                    msg = msg + "node{}: binary(node{}, {})".format(i, idx1 - 4, idx2)
                elif idx2 >= 4:
                    msg = msg + "node{}: binary({}, node{})".format(i, idx1, idx2 - 4)
                else:
                    msg = msg + "node{}: binary({}, {})".format(i, idx1, idx2)
        return msg + "\n"

    def set_active(self):
        self.root.active = True
        queue = []
        visited = [10]
        queue = np.concatenate((queue, np.where(self.adj[-1] != 0)[0].flatten())).tolist()
        self.active_nodes = np.zeros(shape=(9,))
        self.active_nodes[-1] = 1
        while queue:
            node = int(queue.pop(0))
            if node in visited:
                continue
            visited.append(node)
            queue = np.concatenate((queue, np.where(self.adj[node] != 0)[0].flatten())).tolist()
            self.active_nodes[node] = 1
        self.active_nodes = np.asarray(self.active_nodes, dtype=int)
        return

    @staticmethod
    def normalize(x):
        if np.abs(x.max() - x.min()) < 1e-4:
            return x
        return (x - x.min()) / (x.max() - x.min())

    def check_integrity(self):
        eps = 1e-7
        yhat = tf.convert_to_tensor(
            np.vstack((np.linspace(0 + eps, 1 - eps, 1000), 1 - np.linspace(0 + eps, 1 - eps, 1000))).T,
            dtype=tf.float32)
        y = tf.convert_to_tensor(np.asarray([[0, 1] * 1000]).reshape(1000, 2), dtype=tf.float32)
        p = self.call(y, yhat, pred=False).numpy()
        self.phenotype = self.normalize(p)
        if np.argmin(p) in range(490, 510) or np.argmin(-p) in range(490, 510):  # min is to close to 0.5
            return False

        diff = np.diff(p)
        if np.all(diff < 0):
            self.flip = True
            self.phenotype = self.normalize(- p)
            return True
        elif np.all(diff > 0):
            self.flip = False
            return True
        else:
            t = np.sign(diff)
            sz = t == 0  # any zeros
            if np.sum(sz) > 10:  # get rid of platues
                return False
            if np.all(t == 0):  # all zeros
                return False
            while sz.any():
                t[sz] = np.roll(t, 1)[sz]
                sz = t == 0
            if np.sum((np.roll(t, 1) - t) != 0) > 2:  # too many oscillations
                return False
            else:
                if t[2] == -1:
                    self.flip = False
                else:  # parabola is upside down, so flip
                    self.flip = True
                    self.phenotype = self.normalize(-p)
                return True

    def call(self, y_true, yhat, cross_entropy=False, pred=True):

        label_smoothing = tf.convert_to_tensor(self.label_smoothing, dtype=yhat.dtype)
        num_classes = tf.cast(tf.shape(y_true)[-1], yhat.dtype)
        y = y_true * (1.0 - label_smoothing) + (
                label_smoothing / num_classes
        )

        if cross_entropy:
            return -tf.math.reduce_sum(y * tf.math.log(yhat), axis=-1)

        one = tf.constant(1.0, dtype=y.dtype)
        neg_one = tf.constant(- 1.0, dtype=y.dtype)

        res = [y, yhat, one, neg_one] + [None] * 4
        msgs = ["y", "yhat", "1", "-1"] + [None] * 4

        while np.any([j == None for j in res]):
            for i in range(4, 8):
                if res[i] is not None:
                    continue
                if self.active_nodes[i] != 1:
                    res[i] = -1
                    continue
                inds = np.where(self.adj[i] >= 1)[0]
                if len(inds) == 2:
                    if res[inds[0]] is None or res[inds[1]] is None:
                        continue
                    idx1 = np.where(self.adj[i] == 1)[0][0]
                    idx2 = np.where(self.adj[i] == 2)[0][0]
                    t, msg = self.nodes[i - 4].call(res[idx1], res[idx2], msgs[idx1], msgs[idx2])
                else:
                    if res[inds[0]] is None:
                        continue
                    t, msg = self.nodes[i - 4].call(res[inds[0]], None, msgs[inds[0]], None)
                res[i] = t
                msgs[i] = msg

        inds = np.where(self.adj[-1] >= 1)[0]
        if len(inds) == 2:
            idx1 = np.where(self.adj[-1] == 1)[0][0]
            idx2 = np.where(self.adj[-1] == 2)[0][0]
            t, msg = self.root.call(res[idx1], res[idx2], msgs[idx1], msgs[idx2])
        else:
            t, msg = self.root.call(res[inds[0]], None, msgs[inds[0]], None)

        self.msg = msg
        if self.flip:
            if pred:
                return -tf.reduce_mean(tf.reduce_sum(t, axis=-1))
            else:
                return -tf.reduce_sum(t, axis=-1)
        if pred:
            return tf.reduce_mean(tf.reduce_sum(t, axis=-1))
        else:
            return tf.reduce_sum(t, axis=-1)


class GeneticAlgorithmRegularized:

    def __init__(self, gen_size):
        self.gen_size = gen_size
        self.gen = []
        self.fitness = []
        self.prev_individuals = []
        self.best_individuals = []
        self.best_fit = []
        self.mean_fit = []
        self.median_fit = []
        self.min_fit = []
        self.similarities = []
        self.phenotypes = []
        self.functions = []
        self.index = 0  # self.gen_size

        self.init_gen = []
        self.init_fitness = []

    def initialize(self, fitness_function_1, fitness_function_2, init_size):
        msg = "TRAINING INITIAL POPULATION\nUsing Fitness Function 1"
        print(msg)
        logging.info(msg)
        start = time.time()
        self.init_gen = []
        self.init_fitness = []
        for i in range(0, init_size):
            self.init_gen.append(Loss())  # random loss
            result = fitness_function_1(self.init_gen[i].call)
            if result is None:
                msg = " INIT MODEL ARCHITECTURE FAILED..."
                self.init_fitness.append(0)
            else:
                f, v, t, hist = result
                self.init_gen[i].hist = hist
                msg = " MODEL {} -> Val Acc: {}, Val Loss: {}, Time: {}, Fun: {}".format(i, f, v, t, self.init_gen[i].msg)
                self.init_fitness.append(f)
            print(msg)
            logging.info(msg)

        self.init_fitness = np.asarray(self.init_fitness)
        self.init_gen = np.asarray(self.init_gen)
        bst = np.argsort(-self.init_fitness)[0:self.gen_size]
        self.fitness = self.init_fitness[bst]
        self.gen = self.init_gen[bst]

        msg = "TAKING BEST {}\nUSING FITNESS FUNCTION 2".format(self.gen_size)
        print(msg)
        logging.info(msg)
        for i in range(0, self.gen_size):
            result = fitness_function_2(self.gen[i].call)
            if result is None:
                msg = " MODEL ARCHITECTURE FAILED..."
                self.fitness[i] = 0
            else:
                f, v, t, hist = result
                self.gen[i].hist = hist
                msg = " MODEL {} -> Val Acc: {}, Val Loss: {}, Time: {}, Fun: {}".format(i, f, v, t,
                                                                                         self.gen[i].msg)
                self.fitness[i] = f
            print(msg)
            logging.info(msg)

        finish = time.time()
        msg = " Time Elapsed: {} min".format((finish - start) / 60.0)
        print(msg)
        logging.info(msg)

    def evolve(self, max_iter, fitness_function):
        start = time.time()
        for k in range(self.index, self.index + max_iter):

            inds = np.random.choice(range(0, self.gen_size), 20)
            fits = self.fitness[inds]
            bst = np.argmax(fits)
            chosen = self.gen[inds[bst]]
            max_redo = 7
            f = 0
            while max_redo > 0:
                done_mutating = 2500
                while done_mutating > 0:
                    child = copy.deepcopy(chosen)
                    child.age = 0
                    if child.mutate([ind.msg for ind in self.gen], [ind.phenotype for ind in self.gen]):
                        break
                    else:
                        msg = "FAILED MUTATION"
                    done_mutating -= 1
                result = fitness_function(child.call)
                if result is None:
                    max_redo -= 1
                    if max_redo == 0:
                        msg = "CHILD ARCHITECTURE FAILED... {}".format(child.msg)
                        f = 0
                        child.hist = None
                else:
                    f, v, t, hist = result
                    child.hist = hist
                    msg = "CHILD {}-> Val Acc: {}, Val Loss: {}, Time: {}, Fun: {}".format(k, f, v, t, child.msg)
                    break
            msg = " -> Mutation From: {} <-> ".format(chosen.msg) + msg
            print(msg)
            logging.info(msg)

            for i in range(0, self.gen_size):
                self.gen[i].age += 1

            if f == 0:
                fit_mean = np.mean(self.fitness)
                fit_median = np.median(self.fitness)
                fit_min = np.min(self.fitness)
                fit_best = np.max(self.fitness)
                self.best_fit.append(fit_best)
                self.mean_fit.append(fit_mean)
                self.median_fit.append(fit_median)
                self.min_fit.append(fit_min)
                self.prev_individuals.append(child)
                continue

            ages = np.asarray([ind.age for ind in self.gen])
            oldest = np.max(ages)
            oldest = np.where(ages == oldest)[0]
            worst = np.argmin(self.fitness[oldest])
            self.prev_individuals.append(self.gen[oldest[worst]])
            self.fitness[oldest[worst]] = f
            self.gen[oldest[worst]] = child

            fit_mean = np.mean(self.fitness)
            fit_median = np.median(self.fitness)
            fit_min = np.min(self.fitness)
            fit_best = np.max(self.fitness)
            self.best_fit.append(fit_best)
            self.mean_fit.append(fit_mean)
            self.median_fit.append(fit_median)
            self.min_fit.append(fit_min)

            msg = "  Best Fit: {}, Mean Fit: {}, Median Fit: {}, Min Fit: {}".format(fit_best, fit_mean, fit_median,
                                                                                     fit_min)
            print(msg)
            logging.info(msg)

        finish = time.time()

        msg = " Time Elapsed: {} min".format((finish - start) / 60.0)
        print(msg)
        logging.info(msg)
        self.index += max_iter




def create_parser():
    '''
    Create a command line parser for the XOR experiment
    '''
    parser = argparse.ArgumentParser(description='Neural Loss Evolution')
    parser.add_argument('--logs_file', type=str, default='nas_loss_regularized_resnet_randaug_final.log',
                        help='Output File For Logging')
    parser.add_argument('--save_dir', type=str, default='nas_loss_regularized_resnet_randaug_final',
                        help='Save Directory for saving Logs/Checkups')
    parser.add_argument('--save_file', type=str, default='nas_loss_regularized_resnet_randaug_final',
                        help='Save File for Algorithm')

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    gen_size = 100

    logging.basicConfig(filename=args.logs_file, level=logging.DEBUG)

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    algo = GeneticAlgorithmRegularized(gen_size=gen_size)
    algo.initialize(fitness_function_1=fitness_function_resnet_standard,  # fitness_function_convnet_standard
                    fitness_function_2=fitness_function_resnet_rand_aug,  # fitness_function_effnet_rand_aug
                    init_size=1000)
    pickle.dump(algo, open(args.save_dir + "/" + args.save_file + "_init", "wb"))

    start = time.time()
    msg = "--- Starting Evolution ---"
    logging.info(msg)
    print(msg)

    msg = "--- ResNet9V2 ----"
    print(msg)

    for i in range(0, 8):
        algo.evolve(max_iter=500, fitness_function=fitness_function_resnet_rand_aug)  # fitness_function_effnet_rand_aug
        pickle.dump(algo, open(args.save_dir + "/" + args.save_file + "_resnet_{}".format(i), "wb"))

    finish = time.time()
    msg = "--- ENDING Evolution ---"
    print(msg)
    logging.info(msg)
    msg = "--- Total Time Taken: {} min ---".format((finish - start) / 60.0)
    logging.info(msg)
    print(msg)
