def generate_room_identifier(user1_id, user2_id):
    # Sort the user IDs to ensure consistent room ID generation regardless of the order
    sorted_ids = sorted([user1_id, user2_id])

    # Concatenate the sorted user IDs to create the room identifier
    room_identifier = f'room_{sorted_ids[0]}_{sorted_ids[1]}'

    return room_identifier
