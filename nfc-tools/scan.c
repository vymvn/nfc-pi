#include <stdio.h>
#include <nfc/nfc.h>

int main() {
    nfc_device* pnd;
    nfc_target nt;
    nfc_context* context;
    nfc_init(&context);

    if (context == NULL) {
        printf("Error initializing NFC context.\n");
        return 1;
    }

    pnd = nfc_open(context, NULL);

    if (pnd == NULL) {
        printf("Error opening NFC device.\n");
        nfc_exit(context);
        return 1;
    }

    if (nfc_initiator_init(pnd) < 0) {
        printf("Error initializing NFC initiator.\n");
        nfc_close(pnd);
        nfc_exit(context);
        return 1;
    }


    // Poll for ISO14443A (Mifare)
    const nfc_modulation nmMifare = {
        .nmt = NMT_ISO14443A,
        .nbr = NBR_106,
    };

    while (1) {
        if (nfc_initiator_select_passive_target(pnd, nmMifare, NULL, 0, &nt) > 0) {
            printf("UID: ");
            for (size_t i = 0; i < nt.nti.nai.szUidLen; i++) {
                printf("%02X ", nt.nti.nai.abtUid[i]);
            }
            printf("\n");

            printf("ATQA: %04X\n", nt.nti.nai.abtAtqa[0] << 8 | nt.nti.nai.abtAtqa[1]);
            // printf("ATQA: %04X\n", nt.nti.nai.abtAtqa[0]);
            printf("SAK: %02X\n", nt.nti.nai.btSak);

            // If no ATS do not print
            if (*nt.nti.nai.abtAts != 0) {

                // Print ATS (Answer To Select)
                printf("ATS: ");
                for (size_t i = 0; i < nt.nti.nai.szAtsLen; i++) {
                    printf("%02X ", nt.nti.nai.abtAts[i]);
                }
                printf("\n");
            }

            // Determine the card type based on nt.nm.nmt
            switch (nt.nm.nmt) {
                case NMT_ISO14443A:
                    printf("Type: ISO14443A");
                    break;
                case NMT_ISO14443B:
                    printf("Type: ISO14443B");
                    break;
                case NMT_FELICA:
                    printf("Type: FeliCa");
                    break;
                case NMT_JEWEL:
                    printf("Type: Jewel");
                    break;
                case NMT_DEP:
                    printf("Type: NFC-DEP");
                    break;

                default:
                    printf("Type: Unknown\n");
                    break;
            }

            break;

        }
    }

    nfc_close(pnd);
    nfc_exit(context);
    return 0;
}
