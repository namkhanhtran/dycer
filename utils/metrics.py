#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The implementation of evaluation metrics including MRR and Recall
"""


def compute_mrr(candidate_entity, related_entities, top_k=None):
    """
    Return MRR for a given entity in the top k in the returned list
    :param candidate_entity:
    :param related_entities: a list of entities
    :param top_k:
    :return:
    """
    if top_k is None:
        top_k = len(related_entities)

    if candidate_entity not in related_entities:
        return 0.0
    if related_entities[candidate_entity] > top_k:
        return 0.0

    return 1.0 / float(related_entities[candidate_entity] + 1)


def mrr(candidates, related_entities, top_k=None):
    """
    :param candidates:
    :param related_entities:
    :param top_k:
    :return:
    """
    avg_mrr = 0.0
    related_entities = dict([(y, x) for x, y in enumerate(related_entities)])
    for candidate_entity in candidates:
        score = compute_mrr(candidate_entity, related_entities, top_k)
        avg_mrr += score
    avg_mrr /= len(candidates)

    return avg_mrr


def dist_mrr(candidates, related_entities, top_k=None):
    """
    Return mrr scores for each entity in the candidates
    :param candidates:
    :param related_entities:
    :param top_k:
    :return:
    """
    avg_mrr = []
    related_entities = dict([(y, x) for x, y in enumerate(related_entities)])
    for candidate_entity in candidates:
        score = compute_mrr(candidate_entity, related_entities, top_k)
        avg_mrr.append(score)

    return avg_mrr


def dist_recall(candidates, related_entities, top_k=[5, 10, 15, 20, 25, 30, 35, 50]):
    """
    Return average recall scores for each top-k
    :param candidates:
    :param related_entities:
    :param top_k:
    :return:
    """
    recall = []
    for top_k in top_k:
        recall.append(float(len(set(candidates) & set(related_entities[:top_k]))) / len(candidates))
    return recall
