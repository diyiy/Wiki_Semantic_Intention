from itertools import takewhile

# from revscoring.datasources import Datasource, diff
from revscoring import Datasource
from revscoring.features import wikitext

CONTEXT = 100

def get_operations(diff_operations):
    pos, a, b = diff_operations
    return pos, a, b

operations_return = Datasource("operations_return",
                                     get_operations,
                                     depends_on=[wikitext.revision.datasources.diff.operations])

def process_relocation_context(diff_operations):
    ops, a, b = diff_operations
    
    pointer = 0
    contexts = []
    for op in ops:
        if op.name == 'equal':
            if pointer != op.a1:
                context = ''.join(a[max(op.a1, 0): op.a2])
                contexts.append(context)
            
            pointer = op.a2
        else:
            pointer = op.a2
    
    return contexts

def process_operations_with_context(diff_operations):
    ops, a, b = diff_operations

    i = 0
    while i < len(ops):
        op = ops[i]

        if op.name == "delete":
            del_op = op
            if len(ops) > i + 1 and ops[i + 1].name == "insert":
                ins_op = ops[i + 1]

                yield ('replace',
                       [('context', "".join(_get_context_before(a, op.a1))),
                        ('delete', "".join(a[del_op.a1:del_op.a2])),
                        ('insert', "".join(b[ins_op.b1:ins_op.b2])),
                        ('context', "".join(_get_context_after(a, op.a2)))
                       ])

                i += 1  # Increments past ins_op
            else:
                yield ('delete',
                       [('context', "".join(_get_context_before(a, op.a1))),
                        ('delete', "".join(a[del_op.a1:del_op.a2])),
                        ('context', "".join(_get_context_after(a, op.a2)))
                       ])
        elif op.name == "insert":
            yield ('insert',
                   [('context', "".join(_get_context_before(a, op.a1))),
                    ('insert', "".join(b[op.b1:op.b2])),
                    ('context', "".join(_get_context_after(a, op.a2)))
                   ])

        else:  # op.name == "equal"
            yield ('equal', [('context', "".join(a[op.a1:op.a2]))])


        i += 1


def _get_context_before(tokens, pos):
    start = 0
    for i in reversed(range(max(pos-CONTEXT, 0), pos)):
        if "\n" in tokens[i]:
            start = i+1
            break

    return tokens[start:pos]

def _get_context_after(tokens, pos):
    end = len(tokens)
    for i in range(pos+1, min(len(tokens), pos+CONTEXT+1)):
        if "\n" in tokens[i]:
            end = i
            break

    return tokens[pos+1:end]
'''
tokens = ["foo", "bar", "baz", "yerp", "derp", "ferp", "\n\n", "pants", "banana"]
CONTEXT = 5
list(_get_context_before(tokens, 3))
list(_get_context_after(tokens, 3))
'''
operations_with_context = Datasource("operations_with_context",
                                     process_operations_with_context,
                                     depends_on=[wikitext.revision.datasources.diff.operations])

relocation_segments_context =  Datasource("relocation_segments_context",
                                     process_relocation_context,
                                     depends_on=[wikitext.revision.datasources.diff.operations])


def process_operations_context(diff_operations):
    operations, a, b = diff_operations

    contexts = []
    for op in operations:
        if op.name == "insert":
            context = b[max(op.b1 - CONTEXT, 0):op.b2 + CONTEXT]
        elif op.name == "delete":
            context = a[max(op.a1 - CONTEXT, 0):op.a2 + CONTEXT]
        else:
            context = None

        contexts.append(context)

    return contexts

operations_context = Datasource("operations_context",
                                process_operations_context,
                                depends_on=[wikitext.revision.datasources.diff.operations])
"""
Returns contextual information in the form of nearby tokens for each insert and
delete diff operation.  Equal operations correspond to a None context.
"""

def process_added_segments_context(diff_operations, contexts):
    operations, a, b = diff_operations

    added_contexts = []
    for op, context in zip(operations, contexts):
        if op.name == "insert":
            added_contexts.append("".join(context))

    return added_contexts


added_segments_context = Datasource("added_segments_context",
                                    process_added_segments_context,
                                    depends_on=[wikitext.revision.datasources.diff.operations,
                                                operations_context])

"""
Returns contextual information in the form of nearby text content for each segment added
"""


def process_removed_segments_context(diff_operations, contexts):
    operations, a, b = diff_operations

    removed_contexts = []
    for op, context in zip(operations, contexts):
        if op.name == "delete":
            removed_contexts.append("".join(context))

    return removed_contexts


removed_segments_context = Datasource("removed_segments_context",
                                      process_removed_segments_context,
                                      depends_on=[wikitext.revision.datasources.diff.operations,
                                                  operations_context])
"""
Returns contextual information in the form of nearby text content for each
segment removed.
"""
