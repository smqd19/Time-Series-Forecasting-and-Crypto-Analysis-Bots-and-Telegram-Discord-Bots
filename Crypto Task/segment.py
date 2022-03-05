def bottomupsegment(sequence, create_segment, compute_error, max_error):
    """
    Return a list of line segments that approximate the sequence.
    
    The list is computed using the bottom-up technique.
    
    Parameters
    ----------
    sequence : sequence to segment
    create_segment : a function of two arguments (sequence, sequence range) that returns a line segment that approximates the sequence data in the specified range
    compute_error: a function of two argments (sequence, segment) that returns the error from fitting the specified line segment to the sequence data
    max_error: the maximum allowable line segment fitting error
    
    """
    segments = [create_segment(sequence,seq_range) for seq_range in zip(range(len(sequence))[:-1],range(len(sequence))[1:])]
    mergesegments = [create_segment(sequence,(seg1[0],seg2[2])) for seg1,seg2 in zip(segments[:-1],segments[1:])]
    mergecosts = [compute_error(sequence,segment) for segment in mergesegments]

    while min(mergecosts) < max_error:
        idx = mergecosts.index(min(mergecosts))
        segments[idx] = mergesegments[idx]
        del segments[idx+1]

        if idx > 0:
            mergesegments[idx-1] = create_segment(sequence,(segments[idx-1][0],segments[idx][2]))
            mergecosts[idx-1] = compute_error(sequence,mergesegments[idx-1])

        if idx+1 < len(mergecosts):
            mergesegments[idx+1] = create_segment(sequence,(segments[idx][0],segments[idx+1][2]))
            mergecosts[idx+1] = compute_error(sequence,mergesegments[idx])

        del mergesegments[idx]
        del mergecosts[idx]

    return segments