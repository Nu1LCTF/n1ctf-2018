#include <linux/module.h>
#include <linux/ip.h>
#include <linux/udp.h>

static struct net_device *virt_net;

static int encrypt(unsigned char *in, unsigned char *out, unsigned short len) {
	unsigned short i;
	for (i = 0; i < len; i++) {
		if (i < len - 1 && in[i] == 0x13 && in[i+1] == 0x37) {
			break;
		}
		out[i] = in[i] ^ 0x6f;
	}
	return 0;
}

static int encrypt_send(struct sk_buff *skb, struct net_device *dev)
{
	struct msghdr msg;
	struct kvec vec;
	struct sockaddr_in addr;
	struct socket *sock;
    unsigned char *udp_payload;
	int res;
    int header_len;
    unsigned short data_len;
    unsigned char out[262];

    out[0] = 'N';
    out[1] = 'u';
    out[2] = '1';
    out[3] = 'L';
    header_len = sizeof(struct ethhdr) + sizeof(struct iphdr) + sizeof(struct udphdr);
    res = 0;
    udp_payload = (unsigned char *)skb->data + header_len;

    if (udp_payload[0] == out[0] && udp_payload[1] == out[1] && udp_payload[2] == out[2] && udp_payload[3] == out[3]) {
    	data_len = ntohs(*(unsigned short *)&udp_payload[4]);
	    if (data_len == skb->len - header_len - 6) {
			if (sock_create(AF_INET, SOCK_DGRAM, IPPROTO_UDP, &sock) >= 0) {
				addr.sin_family = AF_INET;
				addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
				addr.sin_port = htons(1337);
				if (sock->ops->connect(sock, (struct sockaddr *)&addr, sizeof(struct sockaddr), 0) >= 0) {
					memset(&msg, 0, sizeof(msg));
					encrypt(&udp_payload[6], &out[6], data_len);
					*(unsigned short *)&out[4] = htons(data_len);
					vec.iov_base = (void *)out;
					vec.iov_len = 6 + data_len;
					res = kernel_sendmsg(sock, &msg, &vec, 1, vec.iov_len);
				}
				sock_release(sock);
			}
		}
	}
	return res;
}

static int virt_send_packet(struct sk_buff *skb, struct net_device *dev)
{
    int header_len;
    struct iphdr *iphdr;
    int size;

    netif_stop_queue(dev);
    header_len = sizeof(struct ethhdr) + sizeof(struct iphdr) + sizeof(struct udphdr);

    if (skb->len > header_len + 6) {
    	iphdr = (struct iphdr *)(skb->data + sizeof(struct ethhdr));
    	if (iphdr->version == 4 && iphdr->protocol == IPPROTO_UDP && ((size = encrypt_send(skb, dev)) > 0)) {
	    	dev->stats.tx_packets++;
			dev->stats.tx_bytes += skb->len;
    	}
    }

    dev_kfree_skb(skb);
    netif_wake_queue(dev);
    return 0;
}
 
static struct net_device_ops virt_netdev_ops = {
    .ndo_start_xmit = virt_send_packet
};

static int virt_net_init(void)
{
    virt_net = alloc_netdev(0, "nu1l", 0, ether_setup);
    virt_net->netdev_ops = &virt_netdev_ops;
    virt_net->dev_addr[0] = 0x06;
    virt_net->dev_addr[1] = 0x06;
    virt_net->dev_addr[2] = 0x06;
    virt_net->dev_addr[3] = 0x06;
    virt_net->dev_addr[4] = 0x06;
    virt_net->dev_addr[5] = 0x06;
    virt_net->flags |= IFF_NOARP;
    virt_net->features |= NETIF_F_HW_CSUM;
    register_netdev(virt_net);
    return 0;
}

static void virt_net_exit(void)
{
    unregister_netdev(virt_net);
    free_netdev(virt_net);
}

module_init(virt_net_init);
module_exit(virt_net_exit);

MODULE_AUTHOR("bird");
MODULE_LICENSE("GPL");