import torch

def format_scores(scores, true_index, device):
    score_length = scores.size(0)
    true_tensor = scores[true_index].repeat(score_length)
    binary = torch.ones(score_length).to(device)

    return true_tensor.t(), scores.t(), binary
        
def format_scores_reg(scores, true_index, device):
    target = - torch.ones(scores.size())
    target[true_index] = 1
    target = target.to(device)

    return scores, target

def collate_sgs(sgs, device):
    output = []
    # if sgs is a list of tuples with single elements
    if isinstance(sgs, list):
        for (node, pair, edge) in sgs:
            tensor_pair = pair[0].t().contiguous()
            tensor_pair = tensor_pair.to(device)
            node = node[0].to(device)
            edge = edge[0].to(device)
            output.append((node, tensor_pair, edge))
    # if sgs is a tuple where every element is a big list
    elif isinstance(sgs, tuple):
        nodes, pair_idx, edges = sgs

        for node, pair, edge in zip(nodes, pair_idx, edges):
            tensor_pair = pair.t().contiguous()
            tensor_pair = tensor_pair.to(device)
            node = node.to(device)
            edge = edge.to(device)
            output.append((node, tensor_pair, edge))

    return output

