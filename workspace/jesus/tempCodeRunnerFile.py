        registro_nota.insert(pos, int(arp_nota.get()))
        acum += registro_nota[pos]
        pos += 1
        media = int(acum/pos)