import sys

from boto.sqs.message import RawMessage as SqsMessage
from python_common.collections.trie_set import TrieSet
from aws import USWest2 as AwsConnections
from aws.sqs import cycle_queue
from atrax.frontier.message import unpack_message


def process_message(m, seen_urls):
    try:
        url_info = unpack_message(m)
    except Exception, ex:
        return False

    return True
    # if url_info.id in seen_urls:
    #     return False
    # else:
    #     seen_urls.add(url_info.id)
    #     return True


def print_progress(total_messages, moved_messages):
    sys.stdout.write("\rMoved: %d, Deleted %d" % (moved_messages, total_messages-moved_messages))
    sys.stdout.flush()


def delete_duplicates_from_large_queue(queue, size):
    """
    # SQS limits non-visible messages to no more than 120,000
    # If the queue has more items than that then this less efficient method must be used.
    """
    seen_urls = TrieSet()  # Todo: The TrieSet may not be compact enough for queues of this size
    sqs = AwsConnections.sqs()

    total_messages, moved_messages = cycle_queue(
        sqs, queue, egress_predicate=lambda m: process_message(m, seen_urls), progress_callback=print_progress)
    sys.stdout.write("\n")
    return total_messages - moved_messages


def delete_duplicates_from_small_queue(queue):
    seen_urls = TrieSet()

    visibility_timeout = 1800  # 30 minutes should be more than enough to process 100,000 messages
    ms = queue.get_messages(10, visibility_timeout=visibility_timeout)
    num_deleted = 0
    num_processed = 0
    while ms:
        to_delete = []
        for m in ms:
            body = m.get_body()

            if not process_message(body, seen_urls):
                to_delete.append(m)
            num_processed += 1

        if to_delete:
            queue.delete_message_batch(to_delete)
            num_deleted += len(to_delete)
        print_progress(num_processed, num_processed - num_deleted)
        ms = queue.get_messages(10, visibility_timeout=visibility_timeout)
    return num_deleted


def delete_duplicates(queue):
    queue.set_message_class(SqsMessage)
    size = queue.count()

    # if size < 100000:
    #     return delete_duplicates_from_small_queue(queue)
    return delete_duplicates_from_large_queue(queue, size)


import argparse
import aws.sqs
import boto.exception
from python_common.collections.pickling import pickle_set, unpickle_set


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('job', type=str)
    parser.add_argument('--remove_dups', action='store_true')
    parser.add_argument('--state_file', type=str, default=None)
    args = parser.parse_args()

    state_file_path = args.state_file or (args.job + '_frontier_cleanup.state')
    processed_queues = unpickle_set(state_file_path)

    try:
        # for queue in AwsConnections.sqs().get_all_queues(args.job):
        for queue in [AwsConnections.sqs().lookup("siemens20150201-23_209_11_100")]:
            sys.stdout.flush()
            try:
                if aws.sqs.is_empty(queue):
                    queue.delete()
                    print "Deleted " + queue.name
                else:
                    print "Cleansing " + queue.name
                    sys.stdout.flush()
                    if args.remove_dups:
                        if queue.name in processed_queues:
                            print "Already processed"
                        else:
                            num_deleted = delete_duplicates(queue)
                            print "Deleted %s URLs" % num_deleted

                            processed_queues.add(queue.name)
            except boto.exception.SQSError, ex:
                print ex.message
    finally:
        pickle_set(processed_queues, state_file_path)

if __name__ == "__main__":
    main()
